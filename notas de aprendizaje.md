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


# Qué es y por qué html.parser?:

indica qué motor de análisis (parser) debe usar BeautifulSoup para interpretar el HTML que se descargó.

## ¿Qué es un parser?:

Un parser es un programa que lee y comprende el código HTML, lo convierte en una estructura jerárquica (un árbol DOM) que podemos navegar y manipular fácilmente.

En el caso de BeautifulSoup, podés elegir entre varios parsers, y 'html.parser' es uno de ellos.

## ¿Qué significa 'html.parser'?:

Es el parser HTML interno de Python. Viene incluido con la biblioteca estándar, por eso:

✅ No requiere instalación adicional
✅ Es bastante rápido
✅ Es suficientemente bueno para la mayoría de las páginas simples como books.toscrape.com

# ¿Qué pasa si no lo pongo?

Si no especificás el parser, BeautifulSoup intentará adivinar cuál usar, pero puede lanzar una advertencia o elegir uno inesperado (por ejemplo, si tenés lxml instalado, lo usará).

Es buena práctica siempre especificarlo, para que tu código sea más predecible.


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


# Que es el pip freeze?

Es las caracteristicas globales de tu entorno virtual.


# Qué es un cursor para una base de datos?

Es una herramienta que me permite dar comandos, hacer querys, editar, etc. A mi base de datos desde Python o un archivo de programación.


# Qué es un índice en una base de datos?

Un índice es una estructura que la base de datos crea sobre una o varias columnas de una tabla para acelerar las búsquedas y consultas.


Piensa en él como el índice de un libro real:

Si querés encontrar todas las páginas donde se menciona “SQLite”, no leés todo el libro línea por línea.
Mirás el índice al final, que te dice exactamente en qué páginas aparece “SQLite”.


En bases de datos, funciona igual:

Sin índice: para buscar un autor en la tabla Autores, SQLite tendría que revisar fila por fila toda la tabla.
Con índice: SQLite va directamente a los registros que coinciden con el valor buscado, mucho más rápido.


Características de los índices

Aceleran SELECT y JOIN: especialmente cuando buscás por columnas específicas o combinás tablas.
No cambian los datos: solo crean una referencia.
Ocupan espacio: cada índice extra requiere memoria y algo de almacenamiento.
Impacto en INSERT/UPDATE/DELETE: cada vez que se modifica un dato indexado, el índice también se actualiza, lo que puede ralentizar un poco esas operaciones.


En mi caso:

Libros(Titulo) → índice acelera búsquedas por título.
Autores(Nombre) → índice acelera búsquedas por autor.
Libros_Autores(Libro_Id, Autor_Id) → índice acelera los JOIN entre libros y autores.


💡 Tip: No conviene crear índices en columnas que se actualizan mucho, porque cada inserción o actualización también tiene que actualizar el índice. Pero para tu caso (base de datos de libros que no cambia demasiado seguido) está perfecto.