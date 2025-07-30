import requests
from bs4 import BeautifulSoup
import time

base_url = "https://books.toscrape.com/"
fallidos = []  # Aquí guardamos los links que fallaron

def obtener_html_con_reintentos(url, max_reintentos=5, espera=3):
    intentos = 0
    while intentos < max_reintentos:
        try:
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

# Iteramos por las 50 páginas del catálogo
for i in range(1, 51):  # páginas 1 a 50
    print()
    print(f"Procesando página {i}...")
    print()
    url = f"{base_url}catalogue/page-{i}.html"

    html = obtener_html_con_reintentos(url)
    if html is None:
        print(f"❌ Falló la página {i}, la saltamos.")
        fallidos.append(url_libro)
        continue

    soup = BeautifulSoup(html, 'html.parser')
    libros = soup.find_all('article', class_='product_pod')

    for libro in libros:
        # Título
        titulo = libro.h3.a['title']
        
        # Enlace a la página del libro
        link = libro.h3.a['href']
        # A veces los links son relativos (ej: '../../../...'), arreglamos eso:
        link = link.replace('../../../', '')
        url_libro = base_url + "catalogue/" + link

        html_libro = obtener_html_con_reintentos(url_libro)
        if html_libro is None:
            print(f"❌ Falló: {titulo} (no se pudo recuperar HTML)")
            fallidos.append(url_libro)
            continue

        soup_libro = BeautifulSoup(html_libro, 'html.parser')

        try:
            # Precio
            precio = soup_libro.find('p', class_='price_color').text

            # Categoría
            categoria = soup_libro.find('ul', class_='breadcrumb').find_all('a')[2].text.strip()

            # Calificación
            calificacion_tag = soup_libro.find('p', class_='star-rating')
            clases = calificacion_tag['class']
            calificacion = [c for c in clases if c != 'star-rating'][0]

            # Mostramos por consola
            print(f"{titulo} | {precio} | {categoria} | {calificacion} Stars")

        except Exception as e:
            print(f"⚠️ Error de parsing interno en {url_libro} → {e}")
            fallidos.append(url_libro)

        time.sleep(10)  # pausa entre libros

# Al final mostramos los fallidos
print("\n🔁 Libros que fallaron:")
for f in fallidos:
    print(f)
