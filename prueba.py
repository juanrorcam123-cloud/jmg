import requests
import webbrowser
import os

API_KEY = "ad9c7b13b24f9c633e5064880d4c7512"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def obtener_datos_pelicula(titulo_buscado):
    print(f"Buscando en TMDb: {titulo_buscado}...")
    search_url = f"{BASE_URL}/search/movie"
    params_search = {
        "api_key": API_KEY,
        "query": titulo_buscado,
        "language": "es-ES"
    }
    
    try:
        response_search = requests.get(search_url, params=params_search)
        response_search.raise_for_status()
        resultados = response_search.json()['results']
        
        if not resultados:
            print("No se encontraron películas con ese nombre.")
            return None
        pelicula_id = resultados[0]['id']
        detail_url = f"{BASE_URL}/movie/{pelicula_id}"
        params_detail = {
            "api_key": API_KEY,
            "language": "es-ES",
            "append_to_response": "credits"
        }
        
        response_detail = requests.get(detail_url, params=params_detail)
        data = response_detail.json()
        
        peli_limpia = {
            'titulo': data.get('title', 'Sin título'),
            'sinopsis': data.get('overview', 'Sin sinopsis disponible.'),
            'poster_url': f"{IMAGE_BASE_URL}{data.get('poster_path')}" if data.get('poster_path') else "https://via.placeholder.com/500x750?text=No+Poster",
            'año': data.get('release_date', '????')[:4],
            'directores': [persona['name'] for persona in data['credits']['crew'] if persona['job'] == 'Director'],
            'actores': [persona['name'] for persona in data['credits']['cast'][:5]]
        }
        
        return peli_limpia

    except Exception as e:
        print(f"Error de conexión o API Key inválida: {e}")
        return None

def generar_html(datos):
    if not datos: return

    str_directores = ", ".join(datos['directores']) if datos['directores'] else "Desconocido"
    str_actores = ", ".join(datos['actores']) if datos['actores'] else "No disponibles"

    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prueba TMDb - {datos['titulo']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #141414; /* Color oscuro tipo Netflix */
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }}
        .movie-card {{
            background-color: #1f1f1f;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            width: 800px;
            display: flex; /* Divide la tarjeta en dos columnas */
            overflow: hidden;
            border: 1px solid #333;
        }}
        .poster-container {{
            flex: 0 0 300px; /* Ancho fijo para el poster */
        }}
        .poster-container img {{
            width: 100%;
            height: 100%;
            object-fit: cover; /* Ajusta la imagen sin deformarla */
            display: block;
        }}
        .details-container {{
            padding: 30px;
            flex: 1; /* Ocupa el resto del espacio */
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        h1 {{
            margin-top: 0;
            font-size: 2.5rem;
            color: #e50914; /* Rojo */
        }}
        .meta {{
            font-size: 0.9rem;
            color: #aaa;
            margin-bottom: 20px;
        }}
        h3 {{
            color: #f5c518; /* Amarillo IMDb */
            margin-bottom: 5px;
            margin-top: 15px;
        }}
        p.sinopsis {{
            font-style: italic;
            color: #ccc;
            line-height: 1.6;
        }}
        .people-list {{
            margin: 0;
            padding: 0;
            list-style: none;
            color: #eee;
        }}
    </style>
</head>
<body>
    <div class="movie-card">
        <div class="poster-container">
            <img src="{datos['poster_url']}" alt="Poster de {datos['titulo']}">
        </div>
        <div class="details-container">
            <h1>{datos['titulo']}</h1>
            <div class="meta">Año: {datos['año']}</div>
            
            <h3>Sinopsis</h3>
            <p class="sinopsis">{datos['sinopsis']}</p>

            <h3>Dirección</h3>
            <p>{str_directores}</p>

            <h3>Reparto Principal</h3>
            <p>{str_actores}</p>
        </div>
    </div>
</body>
</html>
"""

    nombre_archivo = "pelicula_tmdb.html"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Archivo '{nombre_archivo}' generado con éxito.")
    
    webbrowser.open('file://' + os.path.realpath(nombre_archivo))

if __name__ == "__main__":
    if API_KEY == "Ingresa API":
        print("")
    else:
        pelicula = "The Nightmare Before Christmas" 
        datos = obtener_datos_pelicula(pelicula)
        generar_html(datos)