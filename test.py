import openai
import os
from dotenv import load_dotenv

# docs=chunkify_postman()
# print("docs",docs)
# Set your API key

load_dotenv()

openai.api_key = "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"
# Optional: use TextLoader for large docs
print("key",openai.api_key)