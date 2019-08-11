import requests
from bs4 import BeautifulSoup

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
distances = []


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


def add_distances():
    global distances
    all = soup.findAll("div", {"class": "ptvParameters col-md-12 col-xs-12"})
    for a in all:
        distance_soup = BeautifulSoup(str(a), 'lxml')
        all_nested_elems = distance_soup.findAll("p")
        for para in all_nested_elems:
            distance_km = para.get_text()
            if "km" in distance_km:
                distances.append(distance_km)
                break


def add_desc():
    global descriptions
    for desc in soup.findAll("p", {"class": "ptvText"}):
        descriptions.append(desc.get_text().strip())


def get_page_count():
    return len(soup.findAll("a", {"class": "paginationDigits"}))
    # no_of_pages = soup.findAll("a", {"class": "paginationDigits"})


# TODO : add new column for storing distance of place from center of city

if r.status_code == 200:
    # print(r.text)
    soup = BeautifulSoup(r.text, 'lxml')
    t = soup.find('div', {"id": "attractionList"})
    print(t)
    no_of_pages = get_page_count()
    addImageUrls()
    add_names()
    add_desc()
    add_distances()
    print(len(names))
    print(len(images))
    print(len(descriptions))
    print(distances)
    # mysql = MysqlDbConnSingleton()
    # names_wiki_urls = {}
    # for place_no in range(0, len(names)):
    #     place_name = names[place_no]
    #     if mysql.name_exists(place_name):
    #         print("already in db")
    #     else:
    #         wiki_data = wikipedia_scraping.search_wiki(place_name, "Hyderabad")
    #         print(wiki_data)
    #         mysql.add_new_place(description=descriptions[place_no], brief_info=wiki_data, name=names[place_no],
    #                             nearest_airport="",
    #                             nearest_bus_terminal="",
    #                             nearest_railway_station="",
    #                             state_name="Telangana", city_name="Hyderabad")
