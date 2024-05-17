from first_step import scrap_book, transform_book, load_book
import requests
from bs4 import BeautifulSoup
from csv import writer

def get_all_book_urls(category_page_soup, page_url):
    '''
    Returns a table of all urls from page soup.
    :param category_url: soup of category.
    :return: Table of all single urls.
    '''
    book_references = category_page_soup.find_all('h3')
    links = []
    for ref in book_references:
        end_of_link = (ref.find('a')['href'])

        base_url = page_url.split('.com')
        # build url from start of category url and end of book url
        link = end_of_link.replace('../../..', base_url[0] + '.com/catalogue')
        links.append(link)

    return links

def init_csv():
    '''
    Delete document from previous execution of code.
    Start new one with header.
    :return:
    '''
    with open('second_step.csv', 'w', encoding='utf-8', newline='') as csvfile:
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

def scrap_category(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text,'html.parser')
    print(f'\n--- Scraping category '+soup.find('h1').text+' ---')
    # If category has multiple pages
    pager = soup.find('ul', {'class': 'pager'})
    if pager is None:
        scrap_page(category_url)
    else:
        #Get number of pages from last text character in page string
        number_of_pages = pager.find('li').text.strip()[-1]
        for i in range(1, int(number_of_pages)+1):
            page_url = category_url.replace('index', f'page-{i}')
            scrap_page(page_url)




def scrap_page(page_url):
    '''
    Returns a table of every book url in the input page.
    :param page_url:
    :return: Table of all book urls
    '''
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text,'html.parser')
    books_urls = get_all_book_urls(soup, page_url)
    for book_url in books_urls:
        soup = scrap_book(book_url)
        data = transform_book(soup, book_url)
        load_book(data)

if __name__  == '__main__':
    init_csv()
    scrap_category('https://books.toscrape.com/catalogue/category/books/travel_2/index.html')
    scrap_category('https://books.toscrape.com/catalogue/category/books/mystery_3/index.html')