# TestPinLabs
Worked with Joshna, Soumya,  
[project]
name = "alopinelabs"
version = "0.1.0"
description = ""
authors = [
    {name = "Soumyadeep143",email = "soumyadeep735221@gmail.com"}
]

[tool.poetry.dependencies]
python = "3.11.3"

# UI/Dashboard/Interaction
streamlit = "*"
streamlit-chat = "*"
plotly = "*"
langchain-community = "*"

# LLM/NLP/RAG
openai = "*"
langchain = "^0.3.25"
chromadb = "*"
faiss-cpu = "*"

# API, Data, Testing
requests = "*"
pydantic = "*"
pytest = "*"
pandas = "*"
ujson = "*"

# Collaboration & Auth
streamlit-authenticator = "*"

# Deployment/Dev Tools
python-dotenv = "*"
uvicorn = "*"
loguru = "*"

# (Optional: if customizing dashboards)
dash = "*"
matplotlib = "*"
seaborn = "*"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

