title: Local RAG with LLM
author: Nathaniel Butterworth
date: 2024-08-21
Category: llm
Tags: python,llm,ai,chatgpt,rag

Don't want to share your private data? You can run your own local LLM to query your own documents in a couple steps with a RAG!

1. Get a local LLM
* Get [Ollama](https://ollama.com/download)
* Follow the instructions to install. 
* Open a Terminal and download a model (e.g. llama3.1).
* And serve the model locally.

```
ollama pull llama3.1
ollama serve
```

2. Get the interface:
We will use [LangChain](https://www.langchain.com/) to handle the [vector store](https://js.langchain.com/v0.1/docs/modules/data_connection/vectorstores/) and Steamlit to give you a fancy front-end to interact with the LLM and data upload.
```
git clone https://github.com/Sydney-Informatics-Hub/LLM-local-RAG/
cd LLM-local-RAG
conda create -n localrag python=3.11 pip
conda activate localrag
pip install langchain streamlit streamlit_chat chromadb fastembed pypdf langchain_community
```

3. Start chatting!
```
streamlit run app.py
```

Upload your docs and start asking questions!

![]({attach}images/chatPDF.png){ width=100% }

