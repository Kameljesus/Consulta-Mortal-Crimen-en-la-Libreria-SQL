import requests
from bs4 import BeautifulSoup
import time

base_url = "https://books.toscrape.com/"
fallidos = []  # Aquí guardamos los links que fallaron

# Iteramos por las 50 páginas del catálogo
for i in range(1, 51):  # páginas 1 a 50
    print()
    print(f"Procesando página {i}...")
    print()
    url = f"{base_url}catalogue/page-{i}.html"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        libros = soup.find_all('article', class_='product_pod')
    
    except Exception as e:
        print(f"❌ Falló la página {i}: {url} → {e}")
        continue  # saltamos a la siguiente página

    for libro in libros:
        # Título
        titulo = libro.h3.a['title']
        
        # Enlace a la página del libro
        link = libro.h3.a['href']
        # A veces los links son relativos (ej: '../../../...'), arreglamos eso:
        link = link.replace('../../../', '')
        url_libro = base_url + "catalogue/" + link

        try: 
            # Entrar a la página del libro
            r_libro = requests.get(url_libro, timeout=10)
            r_libro.raise_for_status()
            soup_libro = BeautifulSoup(r_libro.text, 'html.parser')

            # Precio
            precio = soup_libro.find('p', class_='price_color').text

            # Categoría: está en la segunda <ul class="breadcrumb"> → el 3er <a> contiene la categoría
            categoria = soup_libro.find('ul', class_='breadcrumb').find_all('a')[2].text.strip()

            # Calificación: está en una <p class="star-rating X"> donde X es One, Two, Three...
            calificacion_tag = soup_libro.find('p', class_='star-rating')
            clases = calificacion_tag['class']
            calificacion = [c for c in clases if c != 'star-rating'][0]  # nos quedamos con One, Two, etc.

            # También lo mostramos por consola
            print(f"{titulo} | {precio} | {categoria} | {calificacion} Stars")
            
        except Exception as e:
            print(f"❌ Falló: {titulo} → {e}")
            fallidos.append(url_libro)
            
        time.sleep(10)  # pequeña pausa para no sobrecargar el servidor

# Al final mostramos los fallidos
print("\n🔁 Libros que fallaron:")
for f in fallidos:
    print(f)