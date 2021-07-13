from selenium import webdriver
from bs4 import BeautifulSoup

from tqdm import tqdm
from time import sleep

import json


def get_all_laptops(webdriver_browser):
    urls = [
        ("https://kaspi.kz/shop/c/notebooks/?q=%3AproductClass%3AДля+работы+и+учёбы&page={}", 470),
        ("https://kaspi.kz/shop/c/notebooks/?q=%3AproductClass%3AИгровые&page={}", 180),
        ("https://kaspi.kz/shop/c/notebooks/?q=%3AproductClass%3AУльтрабуки&page={}", 360)
    ]

    laptop_links = {}

    for url, count in urls:
        for page in tqdm(range(count // 12 + 1)):
            webdriver_browser.get(url.format(page))

            soup = BeautifulSoup(webdriver_browser.page_source, features="html.parser")
            links = soup.findAll("a", {"class": "item-card__name-link"})

            for laptop in links:
                laptop_links[laptop.text] = {"link": laptop['href']}

    return laptop_links


def parse_price(price_str):
    price_str = price_str.split()[:-1] # remove tenge sign
    price_str = "".join(price_str) # 500 000 -> 500000

    return float(price_str)


def parse_desc(terms, definitions):
    desc = {}

    for term, definition in zip(terms, definitions):
        desc[term.text.strip()] = definition.text.strip()

    return desc


def parse_laptops(webdriver_browser, laptop_links):
    laptops = {}

    for name, link in tqdm(laptop_links.items()):
        finished = 0
        while finished == 0:
            try:
                webdriver_browser.get(link['link'])
                finished = 1
            except:
                sleep(5)

        soup = BeautifulSoup(webdriver_browser.page_source, features="html.parser")
        price = soup.find("div", {"class": "item__price-once"})
        desc_terms = soup.findAll("span", {"class": "specifications-list__spec-term-text"})
        desc_definitions = soup.findAll("dd", {"class": "specifications-list__spec-definition"})

        if price is None:
            price = soup.find("div", {"class": "sellers-table__price-cell-text"})
            if price is None:
                print(link['link'])
                continue

        laptop = parse_desc(desc_terms, desc_definitions)
        laptop["price"] = parse_price(price.text)
        laptop["link"] = link["link"]

        laptops[name] = laptop

    return laptops


def main(webdriver_browser):
    laptops_links = get_all_laptops(webdriver_browser)
    laptops = parse_laptops(webdriver_browser, laptops_links)

    with open("data/laptops.json", "w") as file:
        json.dump(laptops, file)


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(30)

    main(browser)

    browser.quit()