import requests

API_KEY = "AIzaSyBtCtYz5mtfdSu5VVnv8occ8Lbv_Zym2Qo"
titulo = "A Light in the Attic"
url = "https://www.googleapis.com/books/v1/volumes"
params = {"q": f"intitle:{titulo}", "key": API_KEY, "maxResults": 1}

r = requests.get(url, params=params)
print("Código de respuesta:", r.status_code)
print("JSON devuelto:")
print(r.json())