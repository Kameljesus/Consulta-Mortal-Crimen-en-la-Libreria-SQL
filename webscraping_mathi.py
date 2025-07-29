# Paso 1: Setup y carga de página

import requests
from bs4 import BeautifulSoup

base_url = "https://books.toscrape.com/"
url = base_url + "catalogue/page-1.html"  # empezamos desde la primera página real

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


# Paso 2: Buscar todos los libros de esa página

libros = soup.find_all('article', class_='product_pod')


# Paso 3: Para cada libro, entrar a su página y extraer la info

for i in range(1, 10):  # páginas 1 a 50
    print(f"Procesando página {i}...")
    url = f"{base_url}catalogue/page-{i}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    libros = soup.find_all('article', class_='product_pod')

    for libro in libros:
        # Título
        titulo = libro.h3.a['title']
        
        # Enlace a la página del libro
        link = libro.h3.a['href']
        # A veces los links son relativos (ej: '../../../...'), arreglamos eso:
        link = link.replace('../../../', '')
        url_libro = base_url + "catalogue/" + link

        # Entrar a la página del libro
        r_libro = requests.get(url_libro)
        soup_libro = BeautifulSoup(r_libro.text, 'html.parser')

        # Precio
        precio = soup_libro.find('p', class_='price_color').text

        # Categoría: está en la segunda <ul class="breadcrumb"> → el 3er <a> contiene la categoría
        categoria = soup_libro.find('ul', class_='breadcrumb').find_all('a')[2].text.strip()

        # Calificación: está en una <p class="star-rating X"> donde X es One, Two, Three...
        calificacion_tag = soup_libro.find('p', class_='star-rating')
        clases = calificacion_tag['class']
        calificacion = [c for c in clases if c != 'star-rating'][0]  # nos quedamos con One, Two, etc.

        print(f"{titulo} | {precio} | {categoria} | {calificacion} Stars")
