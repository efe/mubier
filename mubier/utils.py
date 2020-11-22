import time
import requests
import random

from bs4 import BeautifulSoup
from datetime import datetime

def get_proxy_address():
    # https://www.proxynova.com/proxy-server-list/country-tr/
    # https://spys.one/free-proxy-list/TR/
    addresses = [
        "88.255.60.220:8080",
        "195.175.209.194:8080",
        "95.0.66.71:1981",
        "91.93.135.113:8080",
        "176.236.99.204:8080",
        "91.93.156.130:8080",
        "176.235.182.79:8080",
        "95.0.66.73:8080",
        "80.253.247.42:3838"
    ]
    return random.choice(addresses)


def get_today():
    return datetime.now().strftime("%Y-%m-%d")


def get_soup(url):
    try:
        proxy_address = get_proxy_address()
        proxies = {
            "http": proxy_address,
            "https": proxy_address,
        }
        response = requests.get(url, proxies=proxies)
    except requests.exceptions.ProxyError:
        print(f"{url} - Proxy fail: {proxy_address}")
        return get_soup(url)
    print(f"{url} - {response.status_code}")
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        time.sleep(10)
        return get_soup(url)

    return BeautifulSoup(response.text, "html.parser")


def fetch_movies_of_today():
    url = 'https://mubi.com/showing'
    soup = get_soup(url)

    movies = []

    articles = soup.find_all('article')
    articles.pop()
    print(len(articles))

    for article in articles:
        path = article.find_all('a')[0]['href']
        url = 'https://mubi.com' + path
        soup = get_soup(url)

        reference_html_tag_of_rating = soup.find("div", text="/10")

        rating_average = float(reference_html_tag_of_rating.previousSibling.previousSibling.text)
        rating_count = int(reference_html_tag_of_rating.parent.parent.find_all("div")[-1].text.replace(" Ratings", "").replace(",", ""))
        name = soup.title.text.replace(" | MUBI", "")
        image_url = soup.find('link', {'rel': 'image_src'})["href"]
        description = soup.find('meta', {'property': 'og:description'})["content"]

        item = {
            "name": name,
            "rating_average": rating_average,
            "rating_count": rating_count,
            "image_url": image_url,
            "description": description
        }
        print(item)
        movies.append(item)

    movies = (sorted(movies, key=lambda k: k['rating_average']))
    movies = list(reversed(movies))
    return movies