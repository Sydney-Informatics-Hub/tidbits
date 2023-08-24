title: CUDA VS CPU: BERT embedding benchmarks
author: Henry Lydecker
date: 2021-07-23
Category: misc
Tags: python, cuda, pytorch

# cuda-vs-cpu-example

**CUDA is faster than CPU for deep learning, but how fast are we talking about? Let's find out!**

## Introduction

At the core of most of the popular whizbang deep learning methods are complex matrix operations.
These operations are very taxing for CPUs.
However, the architecture of GPUs, particularly NVIDIA's RTX consumer gaming cards and various enterprise cards is far more ammenable to deep learning.

Last year, Chao and I developed a pipeline for using Google's BERT (Bidirectional Encoder Representations from Transformers) to classify different portions of text in academic journal articles.
We used Pytorch and Huggingface's Transformers to implement a pre-trained BERT model that had been trained on scientific texts (SciBERT).
While this pipeline gave us very impressive results, it was extremely CPU intensive.
We ended up having to deploy it at scale on a virtual machine, to prevent melting our MacBooks(I honestly wonder if my aggressive use of BERT on my MacBook contributed to its freaky phantom kernal panics...suffice to say you DO NOT want those!).

All along the way, I kept asking myself: how much faster would this be with CUDA? Without further adieou, let's find out!!!

## Scenario: Using BERT

We built a Python pipeline to generate SciBERT sentence embeddings from full texts of academic journal articles; these embeddings would then be passed to a random forest classifier model to predict whether a particular sentence was conflict of interest, funding statement, or anything else. 


Here's the portion of the pipeline concerned that we are interested in:
```
device = torch.device("cpu")

log = logging.getLogger()
logging.basicConfig(level=logging.INFO)
warnings.filterwarnings("ignore")

ap = argparse.ArgumentParser()
ap.add_argument("--text-dir", default="./texts", type=pathlib.Path)
ap.add_argument(
    "-o",
    "--out-path",
    default="./pickles",
    type=pathlib.Path,
)
args = ap.parse_args()

"""
A function to extract text from Academic pdfs that have been converted into DOCX files.
This function excludes content from the references section onwards.
To include references and onwards, remove the if statements from this function.
"""
# TODO: incorporate pdf -> DOCX conversion via Acrobat Pro API?
# TODO: strip images from text
def getText(filename):
    """
    Extract text from a DOCX file, excluding tables.
    """
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        para.text = re.sub(r"-\n(\w+ *)", r"\1\n", para.text)
        para.text = re.sub(r"\s\s+", " ", para.text)
        para.text = re.sub(r"-\s(\w+ *)", r"\1\n", para.text)
        if para.style.name.startswith("Heading") and para.text.startswith(
            ("References", "references", "REFERENCES", "Bibliography", "Citations")
        ):
            break
        if para.text.startswith(
            ("References", "references", "REFERENCES", "Bibliography", "Citations")
        ):
            break
        fullText.append(para.text.strip("\n"))
    return " ".join(fullText)

def check_if_file_exists(self, pom_file_path, extension):
    return pom_file_path.with_suffix(extension).exists()

def sent_span(temp):
    """
    Perform sentence segmentation, and then generate spans describing these sentences.
    """
    sentences = nltk.sent_tokenize(temp)
    spans = []
    for sent in reversed(sentences):
        st = temp.rfind(sent)
        spans.append((st, st + len(sent)))
        temp = temp[:st]
    spans.reverse()
    return spans


def sents(temp):
    """
    Perform sentence segmentation.
    """
    sentences = nltk.sent_tokenize(temp)
    return sentences


def flatten_text(r):
    """
    Squish the nested sentences.
    """
    data = []
    for i, s in enumerate(r["sent_spans"]):
        temp = {
            "filename": r["filename"].replace(".docx", ""),
            "span": s,
            "location": round(100 * ((s[0] + s[1]) / 2) / r["length"], 2),
            "sentence": r["text"][s[0] : s[1]],
        }
        data.append(temp)
    return pd.DataFrame.from_dict(data)

# SciBERT
tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")
model = AutoModel.from_pretrained("allenai/scibert_scivocab_uncased")

# TODO: check to see if input file has already been turned into a pickle
"""
Loop through files in the text directory:
1. read each one in, 
2. sentence segmentation,
3. tokenize using SciBERT,
4. generate SciBERT embeddings, and 
5. export as pickles.
"""
progress = tqdm(args.text_dir.glob("*.docx"))
for text_path in progress:

    if os.path.isfile(str(args.out_path)+"/"+text_path.name+'.pkl'):
        print(text_path.name+" has already been processed")
        continue

    progress.set_description(text_path.name)


    corpus_list = []
    index = []
    filename = []
    cur_corpus = getText(text_path)
    corpus_list.append(cur_corpus)
    index.append(text_path)
    filename.append(os.path.basename(text_path))

    df = pd.DataFrame(index=index, data={"filename": filename, "text": corpus_list})
    df = df.assign(doc_words=df.text.apply(lambda t: len(t.split())))  # Word Counts
    df = df.assign(
        doc_characters=df.text.str.replace("[\s\n\t]", "").str.len()
    )  # Character Counts
    df = df.assign(sent_spans=df.text.apply(lambda text: sent_span(text)))
    df = df.assign(length=df.text.str.len())
    df = df.assign(sents=df.text.apply(lambda text: sents(text)))

    sent_df = pd.concat([flatten_text(df.loc[idx]) for idx in df.index])

    sent_df["sentence"] = sent_df["sentence"].astype("str")
    sent_df["sentence"] = sent_df["sentence"].apply(
        lambda x: x[:512]
    )  # Cut all character strings to a max length of 512 characters.
    sent_df = sent_df[
        sent_df["sentence"].str.contains("[A-Za-z]", na=False)
    ]  # Remove any rows that contains only non-alphanumeric characters.
    sent_df = sent_df.dropna()  # Remove any lines that are NA.
    sent_df = sent_df.reset_index(drop=True)
    idx = sent_df.index

    tokenized = sent_df["sentence"].apply(
        (lambda x: tokenizer.encode(x, add_special_tokens=True))
    )

    max_len = 0
    for i in tokenized.values:
        if len(i) > max_len:
            max_len = len(i)

    padded = np.array([i + [0] * (max_len - len(i)) for i in tokenized.values])

    attention_mask = np.where(padded != 0, 1, 0)

    # input_ids = torch.tensor(padded)
    input_ids = torch.tensor(padded).to(torch.int64)
    attention_mask = torch.tensor(attention_mask)

    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)

    features = last_hidden_states[0][:, 0, :].numpy()

    features = sent_df.join(pd.DataFrame(features, index=idx), rsuffix="_")

    output_str = str(args.out_path)
    base = os.path.basename(text_path.name)
    text_str = str(base)
    output = base.replace(".docx", ".pickle")
    output = output_str + "/" + output
    with open(output, "wb") as output_file:
        pickle.dump(features, output_file)

```
Ok, that's a lot of stuff to look at. 
Lets just look at the parts that are involved with running PyTorch on either CPU or GPU:

```
    device = torch.device("cpu")
    
    # SciBERT
    tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")
    model = AutoModel.from_pretrained("allenai/scibert_scivocab_uncased")
    
    # input_ids = torch.tensor(padded)
    input_ids = torch.tensor(padded).to(torch.int64)
    attention_mask = torch.tensor(attention_mask)

    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)

    features = last_hidden_states[0][:, 0, :].numpy()
```

With a few simple changes, we can tell our install of PyTorch to use CUDA.

NOTE: on MacOS your PyTorch install will by default be the CPU only version.
To work with CUDA and GPUs, you should use a computer with a compatible GPU and OS (Linux or Windows are the best for now).

```
# Check if you have CUDA available
    if torch.cuda.is_available():
        device = torch.device('cuda:0')
    else:
        device = torch.device('cpu')
        print("You have to use this script on a computer with CUDA")
        exit()
    
    # SciBERT
    tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")
    model = AutoModel.from_pretrained("allenai/scibert_scivocab_uncased").to(device)

    input_ids = torch.tensor(padded).to(device)
    attention_mask = torch.tensor(attention_mask).to(device)
  

    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)

    # Pass tensors back to the cpu for numpy
    features = last_hidden_states[0][:, 0, :].cpu().numpy()
```

## Setup

For this simple comparison, we will be running our example pipeline on two very different computers.
NOTE: these names were invented fo this article.


**1. Computer 1 "Ol'Steevie" - 16 inch Macbook Pro**

  - OS: macOS Big Sur
  - Processor: 2.3 Ghz 8-Core Intel Core i9
  - Memory: 64 GB 2667 MHz DDR4
  - GPU: AMD Radeon Pro 5500M 4 GB (0 CUDA cores)

**2. Computer 2 "Clippy's Revenge" - Henry's home built PC**

  - OS: Windows 10 Home
  - Processor: 3.7 GHz 8-Core AMD Ryzen 7 2700x
  - Memory: 16 GB 3000 MHz DDR4
  - GPU: NVIDIA GeForce RTX 2070 Super 8 GB (2560 CUDA cores)
  
Clever readers will want to ask: why didn't you just run it once with cuda and once without on your desktop?
That makes a lot of sense, and I will do that as well.
However, I think this comparison of my SIH-issued ultra MacBook vs my medium-high end gaming PC is still interesting and relevant to many of us.

## Results

Ol'Steevie: 188 seconds, 9.42 iterations / second
![https://github.sydney.edu.au/hlyd4326/cuda-vs-cpu-example/blob/master/images/Screen%20Shot%202021-07-27%20at%209.33.21%20pm.png](https://github.sydney.edu.au/hlyd4326/cuda-vs-cpu-example/blob/master/images/Screen%20Shot%202021-07-27%20at%209.33.21%20pm.png)


Clippy's Revenge (CUDA): 12 seconds, 1.54 iterations / second
![https://github.sydney.edu.au/hlyd4326/cuda-vs-cpu-example/blob/master/images/bert_cuda_test.PNG](https://github.sydney.edu.au/hlyd4326/cuda-vs-cpu-example/blob/master/images/bert_cuda_test.PNG)

Clippy's Revenge (CPU): 481 seconds, 24.09 iterations / second
![https://github.sydney.edu.au/hlyd4326/cuda-vs-cpu-example/blob/master/images/bert_cpu_test.PNG](https://github.sydney.edu.au/hlyd4326/cuda-vs-cpu-example/blob/master/images/bert_cpu_test.PNG)

## Discussion

What did we learn? 

In this case, using CUDA was **15x faster** than the MacBook, and **40x** faster than using my desktop's CPU!!! 

It is also interesting to see how different CPU performance was between my MacBook and my desktop. 
It appears that the higher speed of my CPU was not sufficient to make up for the huge difference in RAM. 
This also suggests that performance on more typical laptops or desktops will be absolutely atrocious. 

If you use PyTorch already, it is super easy to make the switch to using it with CUDA. 
If you have access to a device with CUDA, it is a no brainer to run your deep learning pipelines on CUDA instead of CPU.

## Further Reading

- [The original paper](https://arxiv.org/abs/1810.04805)
- [An explanation with pictures](https://jalammar.github.io/illustrated-bert/)
- [Hugging Face Transformers](https://huggingface.co/): lots of great pre trained models to choose from!
