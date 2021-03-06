import time
import requests
import random
import pytz

from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def get_turkish_proxy_address():
    # https://www.proxynova.com/proxy-server-list/country-tr/
    # https://spys.one/free-proxy-list/TR/
    addresses = [
        "195.175.209.194:8080",
        "212.175.189.86:8080",
        "212.175.189.86:8080",
    ]
    return random.choice(addresses)


def get_today(timezone="Europe/Istanbul"):
    tz = pytz.timezone(timezone)
    return datetime.now().astimezone(tz).strftime("%Y-%m-%d")

def get_yesterday(timezone="Europe/Istanbul"):
    tz = pytz.timezone(timezone)
    return (datetime.now() - timedelta(days=1)).astimezone(tz).strftime("%Y-%m-%d")


def get_soup(url, use_proxies):
    if use_proxies:
        try:
            proxy_address = get_turkish_proxy_address()
            proxies = {
                "http": proxy_address,
                "https": proxy_address,
            }
            print(f"Going to request with {proxy_address} proxy.")
            response = requests.get(url, proxies=proxies)
            print(f"{url} - {response.status_code} - Proxy: {proxy_address}")
        except requests.exceptions.ProxyError:
            print(f"{url} - Proxy fail: {proxy_address}")
            return get_soup(url, use_proxies)
    else:
        response = requests.get(url)
        print(f"{url} - {response.status_code}")
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        time.sleep(10)
        return get_soup(url, use_proxies)

    return BeautifulSoup(response.text, "html.parser")


def fetch_movies_of_today():
    url = 'https://mubi.com/showing'
    soup = get_soup(url, use_proxies=True)

    movies = []

    articles = soup.find_all('article')
    articles.pop()
    print(len(articles))

    for article in articles:
        path = article.find_all('a')[0]['href']
        url = 'https://mubi.com' + path
        soup = get_soup(url, use_proxies=False)

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

    movies = sorted(movies, key=lambda k: k['rating_count'])
    movies = sorted(movies, key=lambda k: k['rating_average'])
    movies = list(reversed(movies))
    return movies