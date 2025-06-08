from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI
import openai
from preprocess import chunkify_postman
import os
from dotenv import load_dotenv
# Step 1: Load your doc chunks as "documents"
# docs = [
# "Generate Token: POST /api/auth/v1/token ...", # repeat for each endpoint
# "Create Order: POST /api/pay/v1/orders ...",
# # etc...
# ]
docs=chunkify_postman()
print("docs",docs)
# Set your API key
openai.api_key = "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"
# Optional: use TextLoader for large docs
# Step 2: Split documents
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
split_docs = splitter.create_documents(docs)

# Step 3: Create embeddings and vector DB
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(split_docs, embeddings)

# Step 4: Retrieval QA chain
qa = RetrievalQA.from_chain_type(
 llm=ChatOpenAI(model="gpt-4-turbo", temperature=0),
 chain_type="stuff",
 retriever=db.as_retriever()
)

# Step 5: Simulate user query
question = "Show order of v1-250608055159-aa-yRQkiB"
answer = qa.run(question)
print("ans",answer)