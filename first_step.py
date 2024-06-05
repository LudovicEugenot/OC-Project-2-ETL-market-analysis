import requests
from bs4 import BeautifulSoup
from csv import writer
from os import path, mkdir

# Extract
def scrap_book(book_url):
    """
    Gets soup from url.
    :return: Get soup back.
    """
    response = requests.get(book_url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

# Transform
def transform_book(book_soup, url):
    book_title = book_soup.h1.text.strip()
    table = book_soup.find('table', {"class": "table table-striped"})
    rows = table.find_all('tr')
    upc = rows[0].find('td').text
    price_including_tax = rows[3].find('td').text
    price_excluding_tax = rows[2].find('td').text

    number_available = ''
    for char in rows[-2].find('td').text:  #test every char and append the digits from the string
        if char.isdigit():
            number_available += char

    #go to the description header and get next paragraph
    try:
        product_description = book_soup.find('div', {"id": "product_description"}).findNext('p').text
    # for the books without descriptions, we let an empty space instead
    except AttributeError:
        product_description = ''

    #on book pages, the category is 3rd in the breadcrumb
    category = book_soup.find('ul', {'class': 'breadcrumb'}).find_all('li')[2].text.strip()

    #get the number of stars by their color in the page rating
    #rating = book_soup.find('p', {'class': 'star-rating'}).find_all('i', {'style': 'color:#E6CE31'})
    #review_rating = len(rating)

    #get the rating number from the class name
    rating = book_soup.find('p', {'class': 'star-rating'})['class'][-1]
    #would have used a match - case but I'm on 3.9
    if rating == 'Zero':
        review_rating = '0'
    elif rating == 'One':
        review_rating = '1'
    elif rating == 'Two':
        review_rating = '2'
    elif rating == 'Three':
        review_rating = '3'
    elif rating == 'Four':
        review_rating = '4'
    elif rating == 'Five':
        review_rating = '5'
    else:
        review_rating = 'ERROR'

    base_url = url.split('.com')
    #get first image src and build url
    image_url = book_soup.find('img')['src'].replace('../..', base_url[0]+'.com')

    print('Scraping book: '+book_title)
    return [url,
        upc,
        book_title,
        price_including_tax,
        price_excluding_tax,
        number_available,
        product_description,
        category,
        review_rating,
        image_url]

# Load
def load_book(book_data):
    with open('second_step.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = writer(csvfile, delimiter=',')
        csvwriter.writerow(book_data)


def init_csv(document_path, document_title):
    '''
    Delete document from previous execution of code.
    Start new one with header.
    :param document_path:
    :param document_title:
    :return:
    '''
    if not path.exists(document_path):
        recursive_mkdir(document_path)

    with open(f'{document_path}/{document_title}.csv', 'w', encoding='utf-8', newline='') as csvfile:
        csvwriter = writer(csvfile, delimiter=',')
        csvwriter.writerow(['SEP=,'])
        csvwriter.writerow(['product_page_url',
                            'universal_product_code (upc)',
                            'title',
                            'price_including_tax',
                            'price_excluding_tax',
                            'number_available',
                            'product_description',
                            'category',
                            'review_rating',
                            'image_url'])# Write the header

def recursive_mkdir(path):
    # mkdirs doesn't work on Pycharm so I'm coding my own mkdirs
    '''
    Recursively call mkdir to create the directories.
    Made with relative path (with '/') in mind.
    :param path: relative path intended.
    :return:
    '''
    try:
        mkdir(path)
    except FileNotFoundError:
        path_parts = str(path).split('/')
        new_path = '/'.join(path_parts[0:-1])
        recursive_mkdir(new_path)
        mkdir(path)

def main():
    book_url = "https://books.toscrape.com/catalogue/alice-in-wonderland-alices-adventures-in-wonderland-1_5/index.html"
    init_csv('data', 'first_step')

    book_scraped = scrap_book(book_url)
    book_transformed = transform_book(book_scraped, book_url)
    load_book(book_transformed)

if __name__  == '__main__':
    main()