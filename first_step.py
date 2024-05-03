import requests
from bs4 import BeautifulSoup

##book_url = "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"

def scrap_book():
    """
    Gets soup from himalayas url for now though "response".
    :return: Get soup back.
    """
    response = requests.get("https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html")
    # to get input later response = requests.get(input("Paste url of book you want to get the name of."))
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def main():
    book_scraped = scrap_book()
    book_title = book_scraped.title.text
    print(book_title)

if __name__  == '__main__':
    main()