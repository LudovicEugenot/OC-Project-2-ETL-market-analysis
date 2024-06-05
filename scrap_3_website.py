import requests
from bs4 import BeautifulSoup
from scrap_2_category import scrap_category


def scrap_all():
    home_url = 'https://books.toscrape.com/'
    response = requests.get(home_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    category_table = soup.find('ul', {'class': 'nav nav-list'}).find('ul').find_all('li')
    for category in category_table:
        link = home_url + category.find('a')['href']
        scrap_category(link)


if __name__ == '__main__':
    scrap_all()
