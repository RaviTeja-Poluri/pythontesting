import requests
from bs4 import BeautifulSoup


def search_wiki(name, city):
    google_urls = get_google_urls(name)
    return identify_wiki_name_from_urls(google_urls)
    # if city.title() in name:
    #     name = name.replace(city, "")
    # print("searching for", name)
    # try:
    #     print(wikipedia.WikipediaPage(title=name.title()).content.split("== See also ==")[0])
    # except PageError:
    #     search_wiki(name.replace(" ", ""), city)


def identify_wiki_name_from_urls(urls=[]):
    names = []
    for url in urls:
        if "en.wikipedia.org" in url:
            splitted_url = url.split("/")
            names.append(splitted_url[len(splitted_url) - 1])
    return names


def get_google_urls(name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Pragma': 'no-cache'
    }
    url = 'https://www.google.com/search?q=' + name + " wiki"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    t = soup.findAll('cite', {"class": "iUh30"})
    print(t)
    urls = []
    for url in t:
        urls.append(url.get_text().strip())
    return urls
