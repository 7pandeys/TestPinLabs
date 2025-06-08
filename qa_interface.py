import streamlit as st
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import os

# Set your OpenAI key (you should use secrets in production)
os.environ["OPENAI_API_KEY"] = "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"

# Load vectorstore
embedding_model = OpenAIEmbeddings()
vectorstore = FAISS.load_local(
    r"C:\Users\dell\OneDrive\Desktop\alopinelabs\api_vectorstore",
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever()
llm = ChatOpenAI(temperature=0)
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Streamlit UI setup
st.set_page_config(page_title="API Doc Chatbot", page_icon="🤖")
st.title("📘 API Doc Chatbot")
st.markdown("Ask any question about your API documentation (Postman collection).")

# Predefined prompts
st.markdown("#### 🔧 Quick Prompts:")
prompt_options = ["Get Order", "Create Payment", "Check Payment Status", "Cancel Order"]
selected_prompt = st.selectbox("Select a predefined prompt:", [""] + prompt_options)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous conversation
for msg, resp in st.session_state.messages:
    st.chat_message("user").write(msg)
    st.chat_message("assistant").write(resp)

# Use selected prompt or chat input
if selected_prompt:
    default_input = selected_prompt
else:
    default_input = ""

# Chat input
user_input = st.chat_input("Ask something about your Alpine labs API", key="chat_input")

# If selected from prompt box, auto-send that prompt
if selected_prompt and not user_input:
    user_input = selected_prompt

# Handle chat
if user_input:
    st.chat_message("user").write(user_input)
    try:
        answer = qa.run(user_input)
    except Exception as e:
        answer = f"⚠️ Error: {e}"
    st.chat_message("assistant").write(answer)
    st.session_state.messages.append((user_input, answer))
