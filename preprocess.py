import json



# def format_header(headers):
#  return "\n".join([f"- {h['key']}: {h.get('value', '')}" for h in headers if not h.get('disabled', False)])

# def format_body(body):
#  if body.get('mode') == 'raw':
#  return body['raw']
#  return ""

def chunkify_postman():
    with open(r"C:\Users\dell\OneDrive\Desktop\alopinelabs\src\API Collection.json") as f:
        postman_data = json.load(f)
    chunks = []
    for item in postman_data.get('item', []):
        name = item.get('name', '')
        desc = item.get('description', '')
        request = item.get('request', {})
        method = request.get('method', 'GET')
        url = request.get('url', {}).get('raw', '')
        if isinstance(request.get('url', {}), dict):
            url = request['url'].get('raw', '')
            headers = request.get('header', [])
            body = request.get('body', {})
            chunk = f"""### {name}"""
            chunks.append(chunk)
    return chunks