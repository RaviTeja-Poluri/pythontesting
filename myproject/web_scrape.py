import requests
from bs4 import BeautifulSoup

import wikipedia_scraping
from mysql_service import MysqlDbConnSingleton

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Pragma': 'no-cache'
}
url = 'https://www.holidify.com/places/hyderabad/sightseeing-and-things-to-do.html'
r = requests.get(url, headers=headers)
soup = ""
images = []
names = []
descriptions = []


def addImageUrls():
    global images
    imageTags = soup.findAll("input", {"class": "dataHolder"})
    for tag in imageTags:
        imageUrl = tag["data-imgurl"]
        images.append(imageUrl)


def add_names():
    global names
    for tag in soup.findAll("h2", {"class": "ptvObjective"}):
        names.append(tag.get_text().split('.', 1)[1].strip())


def add_desc():
    global descriptions
    for desc in soup.findAll("p", {"class": "ptvText"}):
        descriptions.append(desc.get_text().strip())


def get_page_count():
    return len(soup.findAll("a", {"class": "paginationDigits"}))
    # no_of_pages = soup.findAll("a", {"class": "paginationDigits"})


if r.status_code == 200:
    # print(r.text)
    soup = BeautifulSoup(r.text, 'lxml')
    t = soup.find('div', {"id": "attractionList"})
    print(t)
    no_of_pages = get_page_count()
    addImageUrls()
    add_names()
    add_desc()
    print(len(names))
    print(len(images))
    print(len(descriptions))
    mysql = MysqlDbConnSingleton()
    names_wiki_urls = {}
    for place_no in range(0, len(names)):
        place_name = names[place_no]
        name_urls = wikipedia_scraping.search_wiki(place_name, "Hyderabad")
        names_wiki_urls[place_name] = name_urls
        # mysql.add_new_place(description=descriptions[place_no], name=names[place_no], nearest_airport="", nearest_bus_terminal="",
        #                     nearest_railway_station="",
        #                     state_name="Telangana", city_name="Hyderabad")
    print(names_wiki_urls)
