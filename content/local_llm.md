title: Run chatGPT at home
author: Nathaniel Butterworth
date: 2024-03-28
Category: llm
Tags: python,llm,ai,chatgpt

Don't want to share your private questions with chatGPT? You can run your own local version in a couple steps!

1. Get the interface:
```
git clone https://github.com/oobabooga/text-generation-webui.git
cd text-generation-webui
bash start_macos.sh
```
Replace `_macos.sh` with your appropriate operating system and answer the prompts.

This should install everything you need (on the fisrt run) and launch a server hosting your large language model interface.

2. Open a web browser and navigate to:
```
http://localhost:7860/
```

3. Download a model to run.
The easiest is to copy a link to an llm model hosted on [Hugging Face](https://huggingface.co/TheBloke).
This is daunting as there are thousands to choose from. You are limited by the size of your local GPU, but "bigger" is not always better anyway. Different models may be more powerful at different tasks. If you still can't decide, just get this one:
```
https://huggingface.co/TheBloke/CodeLlama-7B-AWQ
```
In the _Model_ tab, paste the link in the _Download_ box and click the *Download* button.

4. Chat!
Once the download is finished, load the model in and click on the *Chat* tab, and start hacking!
