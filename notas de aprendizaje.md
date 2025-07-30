## Cómo crear un entorno virtual?:

python3 -m venv venv

## Cómo activar un ntorno virtual:

source venv/bin/activate

## ¿Qué es BeautifulSoup?

BeautifulSoup es una librería de Python que te permite leer, explorar y extraer datos fácilmente de archivos HTML o XML.

Imaginá que el HTML es una sopa gigante con etiquetas (<h1>, <p>, <div>, etc.). BeautifulSoup te da una cuchara para navegar esa sopa y sacar justo el pedacito que querés.

# ¿Para qué se usa?

Se usa principalmente para scraping de páginas web, cuando ya tenés el HTML y necesitás encontrar:

    Títulos

    Precios

    Ratings

    Categorías

    Cualquier cosa que esté en el HTML

# Cómo instalarlo?:

pip install beautifulsoup4 requests


# ¿Qué hace .raise_for_status()?

Es un método de los objetos Response de requests que:

    Lanza una excepción (HTTPError) si la respuesta HTTP tiene un código de error (4xx o 5xx).

## ¿Por qué es útil?

Porque no todos los errores se consideran fallos automáticamente en requests.get().

Por ejemplo:

    Si accedes a una página que no existe (404), requests.get(url) no lanza error por sí solo, simplemente te da una respuesta con status_code = 404.

    Pero si haces:

response.raise_for_status()

entonces se lanza un error que puedes capturar en un try/except, como hicimos antes.
