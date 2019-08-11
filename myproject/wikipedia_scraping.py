import requests
import wikipedia
from bs4 import BeautifulSoup

exclusions = ["== See also ==", "== References ==", "== Bibliography ==", "== External links =="]


def search_wiki(name, city):
    google_urls = get_google_urls(name, city)
    names = identify_wiki_name_from_urls(google_urls)
    wiki_data = ""
    for name in names:
        print("---------------------------------------------------")
        print("searching for", name)
        if "Talk" not in name:
            try:
                wiki_content = wikipedia.WikipediaPage(title=name).content
                for exclusion in exclusions:
                    if exclusion in wiki_content:
                        wiki_content = wiki_content.split(exclusion)[0]
                        break
                if city in wiki_content:
                    wiki_data = wiki_content.strip()
                    break
            except wikipedia.PageError:
                print("nothing found")
    return wiki_data


def identify_wiki_name_from_urls(urls=None):
    if urls is None:
        urls = []
    names = []
    for url in urls:
        if "en.wikipedia.org" in url:
            splitted_url = url.split("/")
            names.append(splitted_url[len(splitted_url) - 1])
    return names


def get_google_urls(name, city):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Pragma': 'no-cache'
    }
    url = 'https://www.google.com/search?q=' + name.lower() + " " + city.lower() + " wiki"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    t = soup.findAll('cite', {"class": "iUh30"})
    print(t)
    urls = []
    for url in t:
        urls.append(url.get_text().strip())
    return urls
