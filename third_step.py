from first_step import init_csv
from second_step import scrap_category

def scrap_all():
    scrap_category()

if __name__  == '__main__':
    init_csv('third_step')
    print("Hello third")