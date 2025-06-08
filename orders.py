import requests

MERCHANT_ID = '110553'
AUTH_TOKEN = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJVeDFRWk5ZdDdFcWg2YnNVb2ZpeXdiZkFVY0JTdzB4clVTdlI2WkF2VURBIn0.eyJleHAiOjE3NDkzNjg2MTksImlhdCI6MTc0OTM2MTQxOSwianRpIjoiZmM0NTIxODQtNTAzOC00YjdkLTliY2YtMjEyZGU2MDk1NjljIiwiaXNzIjoiaHR0cDovL2tleWNsb2FrLmtleWNsb2FrLnN2Yy5jbHVzdGVyLmxvY2FsL3JlYWxtcy9rb25nLWF1dGgiLCJzdWIiOiI5OThhMzVjNC0zNzcxLTRiNjYtYTg4MC1jZjI4MWJhOTAyOTEiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiI4NDRkNDBmMC04MWNmLTRlODctOWI4OS05ZjFmMzViODY5MmUiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiYm90QGIxNWFkMTAzLTAwNGUtNDE2Ny04MmYxLWQ0NjhlZWMyZDE3NiIsIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1rb25nLWF1dGgiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwic2NvcGUiOiIiLCJjbGllbnRIb3N0IjoiMTAuMjA4LjkyLjUxIiwiY2xpZW50QWRkcmVzcyI6IjEwLjIwOC45Mi41MSIsImNsaWVudF9pZCI6Ijg0NGQ0MGYwLTgxY2YtNGU4Ny05Yjg5LTlmMWYzNWI4NjkyZSIsImF0dHJzIjp7Im1lcmNoYW50LWlkIjoiMTExMzgzIn19.AAjxOqfSRvdzkTftIy2umaesmdsOKGQaUnk-QbVdjiMUTdQPiBiHgaQ-HjidFNYVgLmAMyQY3kOIP2_dsr1SKOFgHJ-5m2Cp0aFbAwRnnaPOibWmoyYTnMDeSQyJ_6L4HzO7YVBGsMagGHaIE5NTQtUpQxqRJkcF9zRMjIMoFROfa_KNCoa5UVxFvs_oC9dtPGaib_GTMVYCsZi1sf59uCnT7_l5tJO88LoLT_ufEKdk3EN6N-AjbsANCHBDAw0HZrApCof7IPgkhrWUEa19ELgwlfiC5IydvV5xkvEcQ0aN1LTR8P3GHwvWl_8GkmJUEfCRbJSlsv5kt5jRkV0v3Q'
COOKIE = 'TS01922b00=012ce8bebce0b0c60363ded49952700396b8fd3ed58c8ddb45667e53c44bdcc35e56c9005c4a56f29e572ed999e679f039d8d96016'

BASE_URL = 'https://pluraluat.v2.pinepg.in/api/pay/v1/orders'

HEADERS = {
    'Merchant-ID': MERCHANT_ID,
    'Content-Type': 'application/json',
    'Authorization': AUTH_TOKEN,
    'Cookie': COOKIE
}

def get_order(order_id: str):
    url = f"{BASE_URL}/{order_id}"
    response = requests.get(url, headers=HEADERS)
    if response.ok:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}
    
