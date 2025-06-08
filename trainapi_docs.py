import json
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import os


def format_headers(headers):
    return "\n".join(
        [f"- {h['key']}: {h.get('value', '')}" for h in headers if not h.get('disabled', False)]
    )


def format_body(body):
    if not body:
        return ""
    mode = body.get('mode', '')
    if mode == 'raw':
        raw_body = body.get('raw', '')
        try:
            parsed = json.loads(raw_body)
            return json.dumps(parsed, indent=2)  # Prettify JSON body
        except Exception:
            return raw_body
    elif mode == 'formdata':
        return "\n".join(
            [f"{entry['key']}: {entry.get('value', '')}" for entry in body.get('formdata', []) if not entry.get('disabled', False)]
        )
    elif mode == 'urlencoded':
        return "\n".join(
            [f"{entry['key']}: {entry.get('value', '')}" for entry in body.get('urlencoded', []) if not entry.get('disabled', False)]
        )
    return ""


def format_query_params(url_obj):
    if not isinstance(url_obj, dict):
        return ""
    return "\n".join(
        [f"- {q['key']}: {q.get('value', '')}" for q in url_obj.get('query', []) if not q.get('disabled', False)]
    )


def process_item(item):
    name = item.get('name', 'Unnamed Endpoint')
    request = item.get('request', {})
    description = request.get('description') or item.get('description', '')
    if isinstance(description, dict):  # Sometimes it's an object with content
        description = description.get('content', '')

    method = request.get('method', 'GET')
    url_obj = request.get('url', {})
    url = url_obj.get('raw', '') if isinstance(url_obj, dict) else str(url_obj)

    headers = format_headers(request.get('header', []))
    body = format_body(request.get('body', {}))
    query_params = format_query_params(url_obj)

    content = f"""### {name}

**Description:** {description.strip()}

**Method:** {method}  
**URL:** {url}  
"""

    if query_params:
        content += f"\n**Query Parameters:**\n{query_params}\n"
    if headers:
        content += f"\n**Headers:**\n{headers}\n"
    if body:
        content += f"\n**Request Body:**\n{body}\n"

    return Document(page_content=content.strip())


def parse_items(items):
    documents = []
    for item in items:
        if 'item' in item:  # Nested folder
            documents.extend(parse_items(item['item']))
        else:
            doc = process_item(item)
            if doc:
                documents.append(doc)
    return documents


def load_postman_collection(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    items = data.get('item', [])
    return parse_items(items)


def save_docs_to_jsonl(documents, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for doc in documents:
            json_obj = {"text": doc.page_content}
            f.write(json.dumps(json_obj) + "\n")
    print(f"✅ Saved {len(documents)} documents to {output_path}")


def main():
    # Load and process Postman collection
    docs = load_postman_collection(
        r"C:\Users\dell\OneDrive\Desktop\alopinelabs\src\API Collection.json"
    )
    print(f"✅ Loaded {len(docs)} API endpoints.")

    # Save raw docs as JSONL
    save_docs_to_jsonl(docs, "api_docs.jsonl")

    # Split into chunks for embeddings
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs_chunked = text_splitter.split_documents(docs)
    print(f"✅ Split into {len(docs_chunked)} chunks.")

    # Create embeddings and FAISS vector store
    embedding_model = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs_chunked, embedding_model)

    # Save vector store
    vectorstore.save_local("api_vectorstore")
    print("✅ Vector store saved to ./api_vectorstore")


if __name__ == "__main__":
    main()
