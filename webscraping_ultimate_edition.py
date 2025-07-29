# Versión mejorada con manejo de errores y reintentos
import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def crear_sesion_robusta():
    """Crea una sesión con reintentos automáticos"""
    session = requests.Session()
    
    # Configurar estrategia de reintentos
    retry_strategy = Retry(
        total=3,  # 3 reintentos máximo
        backoff_factor=1,  # Tiempo de espera entre reintentos
        status_forcelist=[429, 500, 502, 503, 504],  # Códigos de error para reintentar
    )
    
    # Aplicar la estrategia a la sesión
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Headers para parecer más humano
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    return session

def hacer_request_seguro(session, url, max_reintentos=3):
    """Hace una request con manejo de errores"""
    for intento in range(max_reintentos):
        try:
            response = session.get(url, timeout=10)  # Timeout de 10 segundos
            response.raise_for_status()  # Lanza excepción si hay error HTTP
            return response
        
        except requests.exceptions.RequestException as e:
            print(f"Error en intento {intento + 1}: {e}")
            if intento < max_reintentos - 1:
                tiempo_espera = random.uniform(1, 3)  # Espera aleatoria entre 1-3 segundos
                print(f"Esperando {tiempo_espera:.1f} segundos antes del siguiente intento...")
                time.sleep(tiempo_espera)
            else:
                print(f"Falló después de {max_reintentos} intentos")
                return None

def scrape_libros():
    base_url = "https://books.toscrape.com/"
    session = crear_sesion_robusta()
    
    # Contador de errores
    errores_pagina = 0
    errores_libro = 0
    libros_procesados = 0
    
    # Abrimos el archivo CSV y escribimos la cabecera
    with open("libros.csv", mode="w", encoding="utf-8", newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(["titulo", "precio", "categoria", "calificacion"])
        
        # Iteramos por las 50 páginas del catálogo
        for i in range(1, 51):
            print(f"\n=== Procesando página {i}/50 ===")
            
            url = f"{base_url}catalogue/page-{i}.html"
            response = hacer_request_seguro(session, url)
            
            if response is None:
                print(f"❌ Error: No se pudo cargar la página {i}")
                errores_pagina += 1
                continue
                
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                libros = soup.find_all('article', class_='product_pod')
                
                if not libros:
                    print(f"⚠️  Advertencia: No se encontraron libros en la página {i}")
                    continue
                
                print(f"📚 Encontrados {len(libros)} libros en esta página")
                
                for j, libro in enumerate(libros, 1):
                    try:
                        # Título
                        titulo_element = libro.find('h3')
                        if not titulo_element or not titulo_element.find('a'):
                            print(f"❌ Error: No se pudo obtener título del libro {j}")
                            errores_libro += 1
                            continue
                            
                        titulo = titulo_element.a['title']
                        
                        # Enlace a la página del libro
                        link = titulo_element.a['href']
                        link = link.replace('../../../', '')
                        url_libro = base_url + "catalogue/" + link
                        
                        # Entrar a la página del libro
                        r_libro = hacer_request_seguro(session, url_libro)
                        
                        if r_libro is None:
                            print(f"❌ Error: No se pudo cargar la página del libro '{titulo}'")
                            errores_libro += 1
                            continue
                            
                        soup_libro = BeautifulSoup(r_libro.text, 'html.parser')
                        
                        # Precio
                        precio_element = soup_libro.find('p', class_='price_color')
                        if not precio_element:
                            print(f"❌ Error: No se pudo obtener precio de '{titulo}'")
                            errores_libro += 1
                            continue
                        precio = precio_element.text
                        
                        # Categoría
                        breadcrumb = soup_libro.find('ul', class_='breadcrumb')
                        if not breadcrumb:
                            print(f"❌ Error: No se pudo obtener categoría de '{titulo}'")
                            errores_libro += 1
                            continue
                            
                        links_categoria = breadcrumb.find_all('a')
                        if len(links_categoria) < 3:
                            print(f"❌ Error: Estructura de categoría inesperada para '{titulo}'")
                            errores_libro += 1
                            continue
                            
                        categoria = links_categoria[2].text.strip()
                        
                        # Calificación
                        calificacion_tag = soup_libro.find('p', class_='star-rating')
                        if not calificacion_tag:
                            print(f"❌ Error: No se pudo obtener calificación de '{titulo}'")
                            errores_libro += 1
                            continue
                            
                        clases = calificacion_tag.get('class', [])
                        calificacion_list = [c for c in clases if c != 'star-rating']
                        calificacion = calificacion_list[0] if calificacion_list else 'Unknown'
                        
                        # Escribir al CSV
                        writer.writerow([titulo, precio, categoria, calificacion])
                        libros_procesados += 1
                        
                        print(f"✅ {j:2d}. {titulo[:50]}... | {precio} | {categoria} | {calificacion}")
                        
                        # Pausa pequeña entre libros para no sobrecargar el servidor
                        time.sleep(random.uniform(0.1, 0.3))
                        
                    except Exception as e:
                        print(f"❌ Error procesando libro {j}: {e}")
                        errores_libro += 1
                        continue
                
                # Pausa más larga entre páginas
                if i < 50:  # No pausar después de la última página
                    tiempo_pausa = random.uniform(1, 2)
                    print(f"⏸️  Pausando {tiempo_pausa:.1f} segundos antes de la siguiente página...")
                    time.sleep(tiempo_pausa)
                    
            except Exception as e:
                print(f"❌ Error procesando página {i}: {e}")
                errores_pagina += 1
                continue
    
    # Resumen final
    print(f"\n{'='*50}")
    print(f"🎉 SCRAPING COMPLETADO")
    print(f"📊 Resumen:")
    print(f"   • Libros procesados exitosamente: {libros_procesados}")
    print(f"   • Errores de página: {errores_pagina}")
    print(f"   • Errores de libro individual: {errores_libro}")
    print(f"   • Archivo guardado: libros.csv")
    print(f"{'='*50}")

if __name__ == "__main__":
    scrape_libros()