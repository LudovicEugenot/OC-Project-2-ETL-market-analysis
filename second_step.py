from first_step import scrap_book, transform_book, load_book, init_csv
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

def scrap_category(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text,'html.parser')
    title = soup.find('h1').text
    print(f'\n--- Scraping category ' + title + ' ---')
    init_csv(title)
    # If category has multiple pages
    pager = soup.find('ul', {'class': 'pager'})
    if pager is None:
        scrap_page(category_url, title)
    else:
        #Get number of pages from last text character in page string
        number_of_pages = pager.find('li', {'class': 'current'}).text.strip()[-1]
        for i in range(1, int(number_of_pages)+1):
            page_url = category_url.replace('index', f'page-{i}')
            scrap_page(page_url, title)

def load_category(all_book_data, category_title):
    for book_data in all_book_data:
        for index, data in enumerate(book_data):
            if type(data) is str and '£' in data:
                book_data[index] = book_data[index][1:]

    with open(f'{category_title}.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = writer(csvfile, delimiter=',')
        csvwriter.writerows(all_book_data)


def scrap_page(page_url, category_title):
    '''
    Returns a table of every book url in the input page.
    :param page_url:
    :return: Table of all book urls
    '''
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text,'html.parser')
    books_urls = get_all_book_urls(soup, page_url)
    all_book_data = []
    # load all category in all_book_data (each cell a book)
    for book_url in books_urls:
        soup = scrap_book(book_url)
        all_book_data.append(transform_book(soup, book_url))

    # load all book data to the "category_name".csv
    load_category(all_book_data, category_title)

if __name__  == '__main__':
    scrap_category('https://books.toscrape.com/catalogue/category/books/classics_6/index.html')
    scrap_category('https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html')