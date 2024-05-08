from bs4 import BeautifulSoup
import cloudscraper
import re
import os

url_relleno = "https://www.animefillerlist.com/shows/"
url_busqueda = "https://www.animefillerlist.com/search/node/"


def buscar_serie(anime_name):
    nombre_busqueda = "%20".join(anime_name.split(' '))
    busqueda = url_busqueda + nombre_busqueda
    scraper = cloudscraper.create_scraper()
    web = scraper.get(busqueda)

    if BeautifulSoup(web.text, "html5lib").find_all(string="Your search yielded no results"):
        return None

    else:
        sopa = BeautifulSoup(web.text, "html5lib").find_all("h3")
        for link in sopa:
            serie = link.find("a", href=True)
            if serie.text == anime_name:
                return serie["href"]
            elif len(serie.text) == len(anime_name):
                return serie["href"]


def lista_relleno(url_relleno_serie):
    lista_capitulos_relleno = []
    if url_relleno_serie is None:
        return lista_capitulos_relleno

    scraper = cloudscraper.create_scraper()
    web = scraper.get(url_relleno_serie)
    soup = BeautifulSoup(web.text, "html5lib").find_all("div", "filler")
    if not soup:
        return lista_capitulos_relleno

    capitulos_relleno = soup[0].find("span", "Episodes").text.split(", ")
    for capitulo in capitulos_relleno:
        if re.fullmatch("[0-9]+", capitulo):
            lista_capitulos_relleno.append(int(capitulo))
        else:
            rango_relleno = capitulo.split("-")
            for numero in range(int(rango_relleno[0]), int(rango_relleno[1])):
                lista_capitulos_relleno.append(numero)
    lista_capitulos_relleno.sort()
    return lista_capitulos_relleno
