import requests
from bs4 import BeautifulSoup
from csv import writer

# Extract
def scrap_book(book_url):
    """
    Gets soup from himalayas url for now though "response".
    :return: Get soup back.
    """
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

# Transform
def transform_book(book_soup):
    book_title = book_soup.h1.text.strip()
    table = book_soup.find('table', {"class": "table table-striped"})
    rows = table.find_all('tr')
    upc = rows[0].find('td').text
    return [upc, book_title]

# Load
def load_book(book_data):
    with open('first_step.csv', 'w', newline='') as csvfile:
        csvwriter = writer(csvfile)
        csvwriter.writerow(['universal_product_code (upc)', 'title']) # Write the header
        csvwriter.writerow(book_data)
        

def main():
    book_url = "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"

    book_scraped = scrap_book(book_url)
    book_transformed = transform_book(book_scraped)
    load_book(book_transformed)

if __name__  == '__main__':
    main()