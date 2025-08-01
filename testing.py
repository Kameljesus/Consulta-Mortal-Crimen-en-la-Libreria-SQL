# Importamos BeautifulSoup y requests:
import requests
from bs4 import BeautifulSoup
import time
import csv
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Ponemos el link principal de la página web que queremos:
base_url = "https://books.toscrape.com/"


fallidos = []  # Aquí guardamos los links que fallaron
autores_no_encontrados = []


def buscar_autor(titulo_a_buscar):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": f"intitle:{titulo_a_buscar}", "key": API_KEY, "maxResults": 1}

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "items" in data:
            volumen = data["items"][0]["volumeInfo"]
            autores = volumen.get("authors", ["Desconocido"])
            autor = ", ".join(autores)
        else:
            autor = "No encontrado"
            autores_no_encontrados.append(titulo_a_buscar)
    except Exception:
        autor = "Error API"
        autores_no_encontrados.append(titulo_a_buscar)

    return autor

def obtener_html_con_reintentos(url, max_reintentos=5, espera=3):
    intentos = 0
    while intentos < max_reintentos:
        try:
            # Pedimos el request para que nos dé (nos retorne) el objeto que queremos de la página web: (Si nos da el código 200 (<Response [200]>), significa que todo está bien).
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return r.text  # Devuelve el HTML si todo sale bien
        except requests.exceptions.RequestException as e:
            intentos += 1
            print(f"❌ Error en {url} → {e}")
            print(f"Reintentando ({intentos}/{max_reintentos})...")
            time.sleep(espera)
    print(f"💀 Fallo final: {url}")
    return None  # Si falla todas las veces

# 🔽 Abrimos el archivo CSV al comienzo
with open("libros.csv", mode="w", newline="", encoding="utf-8") as archivo_csv:
    escritor = csv.writer(archivo_csv)
    escritor.writerow(["Título", "Autores", "Categoría", "Calificación", "Precio", "In Stock", "Link"])  # encabezado

    # Iteramos por las 50 páginas del catálogo
    for i in range(1, 51):  # páginas 1 a 50
        print()
        print(f"Procesando página {i}...")
        print()
        url = f"{base_url}catalogue/page-{i}.html"

        html = obtener_html_con_reintentos(url)
        if html is None:
            print(f"❌ Falló la página {i}, la saltamos.")
            fallidos.append(url)  # <- la URL de la página que falló
            continue
        
        # Creamos la clase soup:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Creamos una 'lista' (mejor dicho, un compilado) de todos los libros con sus características:
        libros = soup.find_all('article', class_='product_pod')

        # Sacamos todos los libros uno por uno:
        for libro in libros:  # "Para cada 'libro' en 'todos los libros'"
            
            # Título:
            titulo = libro.h3.a['title']

            # Autores (con la API):
            autores = buscar_autor(titulo)

            # Categoría (requiere entrar al link del libro):
            # Enlace a la página del lib|ro
            link = libro.h3.a['href']

            # A veces los links son relativos (ej: '../../../...'), arreglamos eso:
            link = link.replace('../../../', '')
            url_libro = base_url + "catalogue/" + link 
            
            # 🔽 Descargar y parsear el HTML del libro individual
            html_libro = obtener_html_con_reintentos(url_libro)
            if html_libro:
                soup_libro = BeautifulSoup(html_libro, 'html.parser')
                try:
                    categoria = soup_libro.find('ul', class_='breadcrumb').find_all('a')[2].text.strip()
                except IndexError:
                    categoria = "Desconocida"
            else:
                categoria = "No cargó"

            # Calificación:
            calificacion_stars = libro.find("p", class_="star-rating")["class"][1]

            estrellas_map = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5,
            }

            calificacion = estrellas_map.get(calificacion_stars, 0)  # 0 por defecto si no se encuentra

            # Precio:
            precio = libro.find('p', class_='price_color').text.strip()

            # Disponibilidad (in stock):
            in_stock_tag = libro.find('p', class_='instock availability').text.strip()

            # 💾 Guardamos en el CSV
            escritor.writerow([titulo, autores, categoria, calificacion, precio, in_stock_tag, url_libro])

            # Mostramos por consola
            print(f"{titulo} | {autores} | {categoria} | {calificacion} | {precio} | {in_stock_tag} | {url_libro}")