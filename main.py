import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
import openai
from preprocess import chunkify_postman  # Make sure this returns a list of strings

# Load your environment variables
from dotenv import load_dotenv
import os
load_dotenv()

# Set OpenAI key from environment or directly (not recommended for security)
openai.api_key = "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"

# --- Setup only once ---
@st.cache_resource(show_spinner=False)
def setup_chain():
    # Load documents
    docs = chunkify_postman()
    
    # Split documents
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.create_documents(docs)
    
    # Create embeddings & vector database
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(split_docs, embeddings)
    
    # Create RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4-turbo", temperature=0),
        chain_type="stuff",
        retriever=db.as_retriever()
    )
    return qa_chain

# Setup chatbot
qa_chain = setup_chain()

# --- Streamlit UI ---
st.set_page_config(page_title="API Chatbot", page_icon="🤖", layout="wide")
st.title("🔍 API Documentation Chatbot")
st.markdown("Ask any question about your API endpoints or flows.")

# Chat input
user_input = st.chat_input("Ask a question about the API...")

# Session state to preserve history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for i, chat in enumerate(st.session_state.chat_history):
    with st.chat_message("user"):
        st.markdown(chat["user"])
    with st.chat_message("assistant"):
        st.markdown(chat["bot"])

# Handle new question
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        try:
            response = qa_chain.run(user_input)
        except Exception as e:
            response = f"❌ Error: {str(e)}"

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.chat_history.append({
        "user": user_input,
        "bot": response
    })
