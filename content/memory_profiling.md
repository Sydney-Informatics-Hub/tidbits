title: Memory profiling in Jupyter notebooks
author: Marius Mather
date: 2021-03-31
Category: Python
Tags: python,jupyter,profiling

Issues with memory use can be hard to pin down,
as your program may only show issues after
carrying out multiple memory intensive steps.
Using the `memory_profiler` package in Jupyter
notebooks allows you to generate a quick
summary of which steps consume the most memory.

First, you need to install the package through pip (or conda):

```shell
pip install memory_profiler
```

Then, in your Jupyter notebook, load it as an extension:

```shell
%load_ext memory_profiler
```

In order to profile functions, they have to be imported
from a module outside the notebook. Here, I profiled
a text classification model that involved loading a
fairly large text vectorization model, using it to
convert around 100 messages to vectors, and
then running a classification model on them:

```python
def classify_messages(messages: Sequence[str]) -> np.array:
    bert_vectorizer = BertVectorizer(model='distilbert')
    classifier = load_trained_classifier()

    message_vectors = bert_vectorizer.make_bert_hidden_states(messages)
    # Classifier needs a dummy value for group in the input
    message_vectors = message_vectors.assign(group=0)

    predicted = classifier.predict(message_vectors)
    return predicted
```

To profile this function, you need to call it using
`%mprun`, specifying each individual function that
you want to profile with a `-f` argument:

```python
%mprun -f classify_messages classify_messages(messages)
```

```
Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    68    154.7 MiB    154.7 MiB           1   def classify_messages(messages: Sequence[str]) -> np.array:
    69    680.1 MiB    525.4 MiB           1       bert_vectorizer = BertVectorizer(model='distilbert')
    70    727.0 MiB     46.9 MiB           1       classifier = load_trained_classifier()
    71                                         
    72   2087.8 MiB   1360.8 MiB           1       message_vectors = bert_vectorizer.make_bert_hidden_states(messages)
    73                                             # Classifier needs a dummy value for group in the input
    74   2088.1 MiB      0.3 MiB           1       message_vectors = message_vectors.assign(group=0)
    75                                         
    76   2089.6 MiB      1.4 MiB           1       predicted = classifier.predict(message_vectors)
    77   2089.6 MiB      0.0 MiB           1       return predicted
```

Creating the vectors turned out to be particularly memory intensive,
so I was able to reduce memory use by processing the messages
in chunks:

```python
def classify_messages_chunked(messages: Sequence[str], chunk_size: int = 10) -> np.array:
    bert_vectorizer = BertVectorizer(model='distilbert')
    classifier = load_trained_classifier()

    all_preds = []
    for chunk in split_into_chunks(messages, chunk_size):
        current_vectors = bert_vectorizer.make_bert_hidden_states(chunk)
        current_vectors = current_vectors.assign(group=0)
        predicted = classifier.predict(current_vectors)
        all_preds.append(predicted)
    result = np.concatenate(all_preds)
    return result
```

```python
%mprun -f classify_messages_chunked classify_messages_chunked(messages, chunk_size=20)
```

```
Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    80    153.8 MiB    153.8 MiB           1   def classify_messages_chunked(messages: Sequence[str], chunk_size: int = 10) -> np.array:
    88    687.5 MiB    533.7 MiB           1       bert_vectorizer = BertVectorizer(model='distilbert')
    89    762.8 MiB     75.3 MiB           1       classifier = load_trained_classifier()
    90                                         
    91    762.8 MiB      0.0 MiB           1       all_preds = []
    92    976.8 MiB      0.0 MiB           6       for chunk in split_into_chunks(messages, chunk_size):
    93    976.8 MiB    213.5 MiB           5           current_vectors = bert_vectorizer.make_bert_hidden_states(chunk)
    95                                                 # Classifier needs a dummy value for group in the input
    96    976.8 MiB      0.1 MiB           5           current_vectors = current_vectors.assign(group=0)
    98    976.8 MiB      0.5 MiB           5           predicted = classifier.predict(current_vectors)
    99    976.8 MiB      0.0 MiB           5           all_preds.append(predicted)
   100    976.8 MiB      0.0 MiB           1       result = np.concatenate(all_preds)
   101    976.8 MiB      0.0 MiB           1       return result
```