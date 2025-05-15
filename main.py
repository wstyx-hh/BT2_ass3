import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
import tempfile
import os
import shutil

# Установка эмбеддингов
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Chroma как локальный векторный стор
vectorstore = Chroma(collection_name="constitution", embedding_function=embedding)

# Подключение LLaMA3 через Ollama
llm = OllamaLLM(model="llama3")

# Retrieval QA Chain
qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

# Streamlit UI
st.title("🇰🇿 Kazakhstan Constitution AI Assistant")

# Загрузка PDF
uploaded_files = st.file_uploader("📄 Upload Constitution PDF(s)", type="pdf", accept_multiple_files=True)
if uploaded_files:
    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            temp_path = tmp_file.name
            shutil.copyfileobj(uploaded_file, tmp_file)

        loader = PyPDFLoader(temp_path)
        pages = loader.load_and_split()
        vectorstore.add_documents(pages)
        os.remove(temp_path)

    st.success("✅ Files processed and added to vector store.")

# Вопрос пользователя
question = st.text_input("🔎 Ask your question:")
if question:
    answer = qa.run(question)
    st.markdown(f"**💬 Answer:** {answer}")
