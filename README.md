> [!CAUTION]
> Este proyecto se encuentra descontinuado

# filmaffinity-api

API REST no oficial de Filmaffinity en castellano. Desarrollada desde cero en python.

Puedes encontrar el codigo dockerizado en [DockerHub](https://hub.docker.com/r/dgongut/filmaffinity-api)

## Introducción

Esta es una API REST que utiliza WEB SCRAPING tanto para hacer búsquedas como para extraer información de películas y
series de [Filmaffinity](https://www.filmaffinity.com/es/main.html).

Está preparada tanto para la ejecución en local, como para crear una imagen en docker.

## API-REST

| Método | API         | Parámetros                                                                   | Descripción                                               |
| ------ | ----------- | ---------------------------------------------------------------------------- | --------------------------------------------------------- |
| GET    | /api/search | `query=${patrón a buscar}` | Busca películas y series por título |
| GET    | /api/film   | `id=${id}`                                             | Obtiene datos de una película o serie mediante un ID      |
| GET   | /api/film   | `url="https://www.filmaffinity.com/es/film819745.html"` | Obtiene datos de una película o serie mediante una URL    |

## Ejemplos de uso

### Búsqueda de películas cuyo título coincida con el string de búsqueda introducido

#### Ejemplo 1

GET
[http://localhost:22049/api/search?query=lo%20que%20el%20viento%20se%20llevo](http://localhost:22049/api/search?query=lo%20que%20el%20viento%20se%20llevo)

```json
[
  {
    "api": "/api/film?id=470268",
    "id": "470268",
    "image": "https://pics.filmaffinity.com/gone_with_the_wind-432251527-large.jpg",
    "rating": "7,9",
    "title": "Lo que el viento se llevó",
    "url": "https://www.filmaffinity.com/es/film470268.html",
    "year": "1939"
  },
  {
    "api": "/api/film?id=796616",
    "id": "796616",
    "image": "https://pics.filmaffinity.com/el_viento_se_llevo_lo_que-971298744-large.jpg",
    "rating": "6,0",
    "title": "El viento se llevó lo que",
    "url": "https://www.filmaffinity.com/es/film796616.html",
    "year": "1998"
  },
  {
    "api": "/api/film?id=484826",
    "id": "484826",
    "image": "https://pics.filmaffinity.com/ni_se_lo_llevo_el_viento_ni_punetera_falta_que_hacia-344865791-large.jpg",
    "rating": "--",
    "title": "Ni se lo llevó el viento, ni puñetera falta que hacía",
    "url": "https://www.filmaffinity.com/es/film484826.html",
    "year": "1982"
  }
]
```

### Búsqueda de una película a través de su ID

GET [http://localhost:22049/api/film?id=470268](http://localhost:22049/api/film?id=470268)

```json
{
  "cast": "Vivien Leigh, Clark Gable, Olivia de Havilland, Leslie Howard, Hattie McDaniel, Thomas Mitchell, Barbara O'Neil, Butterfly McQueen, Ona Munson, Ann Rutherford, Evelyn Keyes, Mickey Kuhn, Ward Bond",
  "company": "Selznick International Pictures, Metro-Goldwyn-Mayer (MGM).  Distribuidora: Metro-Goldwyn-Mayer (MGM)",
  "country": "Estados Unidos",
  "credits": "Sidney Howard, Oliver H.P. Garrett, Ben Hecht, Jo Swerling, John Van Druten.  Novela: Margaret Mitchell",
  "director": "Victor Fleming, George Cukor, Sam Wood",
  "duration": "238 min",
  "genre": "Drama. Romance. Aventuras. Guerra de Secesión. Siglo XIX. Drama romántico. Drama sureño. Cine épico",
  "id": "470268",
  "image": "https://pics.filmaffinity.com/gone_with_the_wind-432251527-large.jpg",
  "isDocumentary": false,
  "isFilm": true,
  "isSerie": false,
  "music": "Max Steiner",
  "originalTitle": "Gone with the Wind",
  "photography": "Ernest Haller",
  "rating": "7,9",
  "ratingCount": "60037",
  "summary": "Georgia, 1861. En la elegante mansión sureña de Tara, vive Scarlett O'Hara (Vivien Leigh), la joven más bella, caprichosa y egoísta de la región. Ella suspira por el amor de Ashley (Leslie Howard), pero él está prometido con su prima, la dulce y bondadosa Melanie (Olivia de Havilland). En la última fiesta antes del estallido de la Guerra de Secesión (1861-1865), Scarlett conoce al cínico y apuesto Rhett Butler (Clark Gable), un vividor arrogante y aventurero, que sólo piensa en sí mismo y que no tiene ninguna intención de participar en la contienda. Lo único que él desea es hacerse rico y conquistar el corazón de la hermosa Scarlett. (FILMAFFINITY)",
  "title": "Lo que el viento se llevó",
  "url": "https://www.filmaffinity.com/es/film470268.html",
  "year": "1939"
}
```

### Búsqueda de una película a través de su URL

GET [http://localhost:22049/api/film?url=%22https://www.filmaffinity.com/es/film333451.html%22](http://localhost:22049/api/film?url=%22https://www.filmaffinity.com/es/film333451.html%22)

```json
{
  "cast": "Christopher Plummer, L. Jeffrey Selznick, David O. Selznick, George Cukor, Margaret Mitchell, Victor Fleming, Vivien Leigh, Clark Gable, Olivia de Havilland, Leslie Howard, Butterfly McQueen, Sam Wood, Louis B. Mayer",
  "company": "Turner Entertainment, Daniel Selznick, Metro-Goldwyn-Mayer (MGM)",
  "country": "Estados Unidos",
  "credits": "David Thomson",
  "director": "David Hinton",
  "duration": "124 min",
  "genre": "Documental. Documental sobre cine. Años 30. Telefilm",
  "id": "333451",
  "image": "https://pics.filmaffinity.com/the_making_of_a_legend_gone_with_the_wind_tv-266622348-large.jpg",
  "isDocumentary": true,
  "isFilm": true,
  "isSerie": false,
  "music": "",
  "originalTitle": "The Making of a Legend: Gone with the Wind",
  "photography": "Glenn Roland",
  "rating": "7,4",
  "ratingCount": "88",
  "summary": "Documental que muestra cómo se realizó \"Lo que el viento se llevó\" desde que David O. Selznick compró los derechos de la novela. (FILMAFFINITY)",
  "title": "La realización de una leyenda: 'Lo que el viento se llevó'",
  "url": "https://www.filmaffinity.com/es/film333451.html",
  "year": "1988"
}
```
