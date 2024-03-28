title: Run an chatGPT at home
author: Nathaniel Butterworth
date: 2024-03-28
Category: llm
Tags: python,llm,ai,chatgpt

Don't want to share your private questions with chatGPT, you can run your own local version in a couple steps!

```
git clone https://github.com/oobabooga/text-generation-webui.git
cd text-generation-webui
bash start_macos.sh

Open a web browser and navigate to:
http://localhost:7860/?__theme=dark

Download a model to run (this is daunting, but if you can't decide, just get this one):

https://huggingface.co/TheBloke/CodeLlama-7B-AWQ

Click on chat and you are good to go!
```
