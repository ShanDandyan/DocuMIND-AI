# DocuMind AI

A RAG (Retrieval-Augmented Generation) system that lets you upload a PDF and ask questions about its content. Built to understand how document retrieval, embeddings, and LLM-based generation work together end-to-end.

## How it works

1. Upload a PDF document
2. The document is split into chunks and converted into vector embeddings
3. Embeddings are stored in a FAISS vector index
4. When you ask a question, the most relevant chunks are retrieved from the index
5. Those chunks are passed as context to an LLM (via Groq), which generates an answer grounded in the document

## Tech stack

- **Streamlit** — user interface
- **LangChain** — document loading and text splitting
- **HuggingFace (`all-MiniLM-L6-v2`)** — text embeddings
- **FAISS** — vector similarity search
- **Groq (Llama 3.1)** — LLM for answer generation

## Screenshots

<img width="1045" height="496" alt="image" src="https://github.com/user-attachments/assets/6d0ee0de-430e-4a39-b0b1-406b35d8e4e3" />

<img width="1761" height="900" alt="image" src="https://github.com/user-attachments/assets/3419a369-9007-49f9-86c5-4ad91c5c99c7" />

<img width="1616" height="892" alt="image" src="https://github.com/user-attachments/assets/a9ddef5c-a871-4548-9e0f-6e0724665c8b" />


## Running locally

1. Clone the repo
   ```
   git clone https://github.com/ShanDandyan/DocuMIND-AI.git
   cd DocuMIND-AI
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Run the app
   ```
   streamlit run app.py
   ```

4. Enter your own Groq API key in the app (get a free one at [console.groq.com](https://console.groq.com)), upload a PDF, and start asking questions.

## Notes and current limitations

- Each question is answered independently — the system does not currently retain conversation history across questions.
- Users provide their own Groq API key; no key is stored or hardcoded in the app.
- Built primarily as a learning project to understand the RAG pipeline end-to-end, rather than as a production-ready tool.

## Possible future improvements

- Conversation memory across follow-up questions
- Support for multiple document uploads
- Display of retrieved source chunks/pages alongside answers
