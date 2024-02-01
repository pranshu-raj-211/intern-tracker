import requests
from bs4 import BeautifulSoup

url = ""
filepath = ""


def get_page(url, refresh=False):
    if refresh:
        response = requests.get(url)
        return BeautifulSoup(response, "lxml")
    return None


def parse(soup):
    container = soup.find_all()
    jobs = {}
    return jobs


def main():
    test = int(input("Offline ? "))
    if test:
        with open(filepath) as f:
            page = f.read()
        jobs = parse(page)
    else:
        page = get_page(url)
        jobs = parse(page)
