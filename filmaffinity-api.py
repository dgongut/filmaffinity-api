from flask import Flask, request, jsonify
from config import *
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)

@app.route('/api/search', methods=['GET'])
def search():
    headers = {"user-agent": USER_AGENT}
    query = request.args.get('query')
    if not query:
        msg = {"error": "The query parameter must contain the information to be searched for."}
        return jsonify(msg), STATUS_CODE_ERROR

    url = f'{URL_SEARCH_FILMAFFINITY}{query}'
    res = requests.get(url, headers=headers, timeout=10)

    elements = []
    response = []

    if res.status_code != 200:
        msg = {"error": f"filmaffinity error: {res.status_code}"}
        return jsonify(msg), STATUS_CODE_ERROR
    else:
        # Búsqueda correcta, analizamos los resultados
        elements = web_scrapping_filmaffinity_search_page(res.text)

    if elements:
        response = []
        for element in elements:
            try:
                filmCode = url_to_film_code(element[1])
            except:
                continue

            responseItem = {
                "id": filmCode,
                "api": f'/api/film?id={filmCode}',
                "title": element[0],
                "url": element[1],
                "rating": element[2],
                "year": element[3],
                "image": element[4]
            }
            response.append(responseItem)

        return jsonify(response), STATUS_CODE_OK

    else:
        # Sin lista: puede que sea página ficha única
        details = web_scrapping_filmaffinity_main_page(res.text)
        if details[0]:  # título existe
            try:
                filmCode = url_to_film_code(details[1])
            except:
                filmCode = None

            responseItem = {
                "id": filmCode,
                "api": f'/api/film?id={filmCode}' if filmCode else None,
                "title": details[0],
                "url": details[1],
                "rating": details[2],
                "year": details[3],
                "image": details[4]
            }
            return jsonify([responseItem]), STATUS_CODE_OK  # siempre un array

        else:
            return jsonify({"error": "Sin resultados"}), STATUS_CODE_NOT_FOUND

@app.route('/api/film', methods=['GET'])
def filmById():
    headers = {"user-agent": USER_AGENT}
    urlParameter = request.args.get('url')
    id = request.args.get('id')
    if urlParameter:
        id = url_to_film_code(urlParameter)

    if not id:
        msg = {"error": "The id or url parameter is required. Try /api/search endpoint to obtain the id."}
        return jsonify(msg), STATUS_CODE_ERROR

    url = f'{URL_FILMAFFINITY_FILM_PAGE}{id}.html'
    res = requests.get(url, headers=headers, timeout=10)

    element = []
    response = []

    if res.status_code != 200:
        msg = {"error": f"filmaffinity error: {res.status_code}"}
        return jsonify(msg), STATUS_CODE_ERROR
    else:
        # Búsqueda correcta, analizamos el resultado
        element = web_scrapping_filmaffinity_main_page(res.text)

    response = {
        "id": id,
        "title": element[0],
        "url": element[1],
        "rating": element[2],
        "year": element[3],
        "image": element[4],
        "originalTitle": element[5],
        "country": element[6],
        "director": element[7],
        "genre": element[8],
        "company": element[9],
        "summary": element[10],
        "cast": element[11],
        "credits": element[12],
        "photography": element[13],
        "music": element[14],
        "ratingCount": element[15],
        "duration": element[16],
        "isFilm": element[17],
        "isSerie": element[18],
        "isDocumentary": element[19]
    }

    return jsonify(response), STATUS_CODE_OK

def web_scrapping_filmaffinity_search_page(htmlText):
    soup = BeautifulSoup(htmlText, "html.parser")
    filmaffinityElements = []

    # Encontrar todas las tarjetas de películas
    movie_cards = soup.find_all('div', class_='d-flex')

    for card in movie_cards:
        # 📌 Imagen
        image = ""
        poster_div = card.find('div', class_='mc-poster')
        if poster_div:
            img_tag = poster_div.find('img')
            if img_tag:
                srcset = img_tag.get('data-srcset', '').strip()
                if srcset:
                    # Separar las distintas opciones en srcset
                    srcset_options = srcset.split(", ")
                    for option in srcset_options:
                        # Verificar si la opción contiene una URL
                        url = option.split(" ")[0]
                        if 'large' in url:
                            image = url
                            break

        # 📌 Título y URL
        title = "Título no disponible"
        url = ""
        title_div = card.find('div', class_='mc-title')
        if title_div:
            link = title_div.find('a')
            if link:
                title = link.get_text(strip=True)
                url = link.get('href', '').strip()
                # Si la URL es relativa, agregamos la base
                if url.startswith('/'):
                    url = f"https://www.filmaffinity.com{url}"

        # 📌 Año
        year = ""
        year_div = card.find('div', class_='ye-w')
        if year_div:
            year = year_div.get_text(strip=True)

        # 📌 Rating
        rating = ""
        rating_div = card.find('div', class_='avg mx-0')
        if rating_div:
            rating = rating_div.get_text(strip=True)

        # 📌 Agregamos la película a la lista
        try:
            url_to_film_code(url)
            filmaffinityElements.append((title, url, rating, year, image))
        except:
            # Si no se puede extraer el código de la película, ignoramos este elemento
            continue

    return filmaffinityElements

def web_scrapping_filmaffinity_main_page(htmlText):
    soup = BeautifulSoup(htmlText, "html.parser")
    # Title
    title = None
    try:
        title = soup.find('h1').find('span').get_text().strip()
    except:
        title = ""

    # Movie Type  
    isFilm = False
    isSerie = False
    isDocumentary = False

    # Buscar el elemento con la clase 'movie-type'
    movie_type_tag = soup.find('span', class_='movie-type')

    if movie_type_tag:
        type_tags = movie_type_tag.find_all('span', class_='type')
        if type_tags:
            for type_tag in type_tags:
                type_text = type_tag.get_text(strip=True).lower()
                if 'serie' in type_text or 'miniserie' in type_text:
                    isSerie = True
                elif 'documental' in type_text:
                    isDocumentary = True
    if not isSerie:
        isFilm = True
    
    # URL
    allLinks = soup.find_all('a')
    url = None
    for link in allLinks:
        if 'Ficha' in link.get_text():
            url = link['href']
            break
    
    # Rating
    rating = None
    try:
        rating = soup.find(id="movie-rat-avg").get_text().replace("  ", "").strip()
    except:
        rating = "--"

    # Image
    image = soup.find('a', class_="lightbox")['href']

    dtElements = soup.find_all('dt')
    ddElements = soup.find_all('dd')
    data = {}
    for dt, dd in zip(dtElements, ddElements):
        key = dt.text
        value = dd.text
        data[key] = value

    # Original Title
    originalTitle = None
    try:
        originalTitle = data["Título original"].strip().replace(".", ",")
    except:
        originalTitle = ""

    # Year
    year = None
    try:
        year = data["Año"].strip()
    except:
        year = ""

    # Country
    country = None
    try:
        country = data["País"].strip()
    except:
        country = ""

    # Directors
    director = None
    try:
        director = data["Dirección"].strip()
    except:
        director = ""

    # Genre
    genre = None
    try:
        genre = re.sub(r'\s+', ' ', re.sub(r'\s*\|\s*', '. ', data["Género"])).strip()
    except:
        genre = ""

    # Company
    company = None
    try:
        company = data["Compañías"].strip()
    except:
        company = ""

    # Summary
    summary = None
    try:
        summary = data["Sinopsis"].strip()
    except:
        summary = ""

    # Cast
    cast = None
    try:
        castElement = soup.find('dd', class_="card-cast-debug")
        castArray = castElement.find_all('a')
        names = [a.get('title') for a in castArray if a.get('title')]
        cast = ", ".join(names)
    except:
        cast = ""

    # Credits
    credits = None
    try:
        credits = data["Guion"].strip()
    except:
        credits = ""

    # Photography
    photography = None
    try:
        photography = data["Fotografía"].strip()
    except:
        photography = ""

    # Music
    music = None
    try:
        music = data["Música"].strip()
    except:
        music = ""

    # Rating count
    ratingCount = None
    try:
        ratingCountElement = soup.find(id="movie-count-rat")
        ratingCount = ratingCountElement.find('span')['content']
    except:
        ratingCount = "0"

    # Duration
    duration = None
    try:
        duration = data["Duración"].strip().replace(".", "")
    except:
        duration = ""

    return [title, url, rating, year, image, originalTitle, country, director, genre, company, summary, cast, credits, photography, music, ratingCount, duration, isFilm, isSerie, isDocumentary]

def url_to_film_code(url):
    numeroPelicula = re.search(r'film(\d+)\.html', url)
    if numeroPelicula:
        numeroPelicula = numeroPelicula.group(1)
        return numeroPelicula
    else:
        raise ValueError(f'No se encontró un número de película en el enlace: {url}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=22049)
