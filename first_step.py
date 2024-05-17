import requests
from bs4 import BeautifulSoup
from csv import writer

# Extract
def scrap_book(book_url):
    """
    Gets soup from url.
    :return: Get soup back.
    """
    response = requests.get(book_url)
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
    product_description = book_soup.find('div', {"id": "product_description"}).findNext('p').text

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
    for index, data in enumerate(book_data):
        if type(data) is str and ('£' or '€') in data:
            book_data[index] = book_data[index][1:]

    with open('second_step.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = writer(csvfile, delimiter=',')
        csvwriter.writerow(book_data)
def init_csv(document_title):
    '''
    Delete document from previous execution of code.
    Start new one with header.
    :return:
    '''
    with open(f'{document_title}.csv', 'w', encoding='utf-8', newline='') as csvfile:
        csvwriter = writer(csvfile, delimiter=',')
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

def main():
    init_csv('first_step')
    book_url = "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"

    book_scraped = scrap_book(book_url)
    book_transformed = transform_book(book_scraped, book_url)
    load_book(book_transformed)

if __name__  == '__main__':
    main()