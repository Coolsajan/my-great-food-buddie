# 🍔 Food Buddiie - RAG + LLM Restaurant Review Chatbot

Food Buddiie is an intelligent chatbot that helps users explore restaurant reviews using a **Retrieval-Augmented Generation (RAG)** pipeline. It combines **Chroma DB** for storing and retrieving restaurant review embeddings with **LLaMA 3** for generating conversational responses. Built with **Streamlit** and deployed on **Hugging Face Spaces**.

---

## 🚀 Features

- 🔎 **RAG Pipeline**: Retrieves relevant reviews based on your query.
- 🧠 **LLM-Powered**: Uses LLaMA 3 to generate human-like responses.
- 🗂 **Chroma DB**: Fast and scalable vector store for text embeddings.
- 💬 **Streamlit UI**: Clean and interactive chat-based frontend.
- ☁️ **Hugging Face Spaces Deployment**: Easily deployable via GitHub Actions.

---

## 🧱 Tech Stack

- `LLaMA 3` (Meta)
- `Chroma DB`
- `sentence-transformers` for embeddings
- `Streamlit` for frontend
- `Hugging Face Spaces` for deployment

---

## 🏗 Architecture Overview

1. **User Input** → via Streamlit chat interface
2. **Query Embedding** → converts input to vector using sentence-transformers
3. **Chroma DB** → retrieves top-k similar reviews
4. **LLM Prompting** → builds a prompt using retrieved texts
5. **LLaMA 3** → generates a detailed response
6. **Display** → renders the response in the chat interface

---

## 📦 Installation

```bash
git clone https://github.com/your-username/food-buddiie.git
cd food-buddiie
pip install -r requirements.txt
```
