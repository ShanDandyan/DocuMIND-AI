import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from groq import Groq
from langchain_community.vectorstores import FAISS
import tempfile
import os

st.title("DocuMIND AI")
st.write(" This is basic RAG system you need to upload your Groq api key to use ")
API_KEY=st.text_input("Enter you groq api here",type="password")
st.caption("Get your free api key at [consol.groq.com](https://console.groq.com)")

Uploaded_pdf=st.file_uploader("Upload your pdf here",type="pdf")
if "db" not in st.session_state:
    if Uploaded_pdf is not None:
        with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as temp_file:
            temp_file.write(Uploaded_pdf.getvalue())
            temporarypath=temp_file.name

        loader=PyPDFLoader(temporarypath)
        data=loader.load()

        if os.path.exists(temporarypath):
            os.remove(temporarypath)

        splitter=RecursiveCharacterTextSplitter( chunk_size=1000,chunk_overlap=200)
        chunks=splitter.split_documents(data)

        embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        st.session_state["db"]=FAISS.from_documents(chunks,embeddings)
        st.write("File uploaded successfully")
if "db" not in st.session_state:
    st.error("please upload a pdf first")
elif not API_KEY:
    st.error("please enter api key")    
else:    
    question =st.text_area("Enter you question here")
    submit=st.button("Get answer")
    if submit:
        answer=st.session_state["db"].similarity_search(question,k=3)
        for i,text in enumerate(answer):
            page_num=text.metadata.get("page","unknown")
            st.write(f"\n---- #match{i+1} found at page number {page_num}")
            st.write(f"\n content: {text.page_content[:250]}--")
            st.write("-"*40)
        context="\n\n".join([chunk.page_content for chunk in answer])   
        client=Groq(api_key=API_KEY)
        response=client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role":"system","content":"You are a precise academic study assistant. Use the provided context fragments "
            "extracted from the PDF documents to write a clear, accurate answer to the user's question. "
            "If the answer cannot be determined from the context, state that you do not know.\n\n"
            },
                {"role":"user","content":f"\n context:\n{context}\n\nquestion: {question}"}
        ])
        st.success(response.choices[0].message.content)

