import os
import pandas
from playwright.sync_api import sync_playwright
from requests_html import HTMLSession, HTML

from db import Product, insert_to_database, engine

BASE_URL = "https://www.superselectos.com/"
PROGRESS_FILE = 'proceed_urls.txt'


def get_category_url(main_url: str) -> dict[str, str]:
    """
    Fetch all categories URL form main page
    :param main_url: URL of main page
    :return: Dict of category name and its URL
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={
                'width': 1920,
                'height': 1080,
            })
        page = context.new_page()

        page.goto(main_url, wait_until='domcontentloaded')

        while True:
            if 'rz-dialog rz-modal-image-viewer rz-modal-centered' in page.content():
                add_exit(page)
                continue
            break

        page.reload()
        page.get_by_role('button', name='Todas las Categorías').click(button='left')

        page.wait_for_selector('div.cat-level-content ul li')

        cat = page.locator('div.cat-level-content ul li').all()
        categories = {}
        for i in cat:
            i.hover()
            page.wait_for_selector('div.cats-groups')
            page.wait_for_timeout(3000)
            cat_element = page.locator('div.cats-groups ul li a').all()
            cat_url = [i.get_attribute('href').replace('/', BASE_URL) for i in cat_element]
            cat_name = [i.inner_text() for i in cat_element]
            merge_cat = dict(zip(cat_name, cat_url))

            categories.update(merge_cat)

        return categories


def add_exit(page):
    """
    Function to press cross-button if an advertisement shown at the beginning of the page
    :param page: where the ads appear
    :return: None
    """
    page.locator('a[class="rz-dialog-titlebar-icon rz-dialog-titlebar-close"]').click()


def get_product_url(url_category: str) -> list[str]:
    """
    Fetch URL of the product after choosing category
    :param url_category: Url from the category to fetch
    :return: List of product URL
    """
    session = HTMLSession()
    response = session.get(url_category)
    product_url = response.html.find('.productos-page-inner .item-producto .prod-nombre .clickeable')
    product_url = [list(i.links) for i in product_url]
    product_url = [i[0] for i in product_url]
    return product_url


def get_html_product(url_product: str) -> HTML:
    """
    Get HTML from the product page
    :param url_product: URL of the product
    :return: DOM tree of HTML
    """
    session = HTMLSession()
    response = session.get(url_product)

    html = response.html

    return html


def check_page(category_url: str) -> bool:
    """
    Check whether a category has multiple page
    :param category_url: URL to check
    :return: Bool
    """
    session = HTMLSession()
    response = session.get(category_url)

    if response.html.find('ul[class="pagination justify-content-end"]'):
        return True
    return False


def get_all_page(category_url: str) -> list[str]:
    """
    Fetch page numbers
    :param category_url: category to get the page number
    :return: List of page number as a string
    """
    session = HTMLSession()

    response = session.get(category_url)

    page = [i for i in response.html.find('ul[class="pagination justify-content-end"]', first=True).text.split() if
            i.isdigit()]

    return page


def product_parser(html_page: HTML, category_url: str, category_name: str) -> None:
    """
    Function to parse the HTML page
    :param html_page: the HTML page
    :param category_url: category url of the current product
    :param category_name: category name of the current product
    :return: A dictionary containing product information
    """
    name = html_page.find('h1[class="det-nom"]', first=True).text if html_page.find('h1[class="det-nom"]',
                                                                                    first=True) else None
    current_price = html_page.find('div[class="info-middle mb-2"] div[class="right"] span.precio',
                                   first=True).text if html_page.find(
        'div[class="info-middle mb-2"] div[class="right"] span.precio', first=True) else None
    actual_price = html_page.find('div[class="col-md-6 det-info"] span[class="antes"]', first=True).text if (
        html_page.find('div[class="col-md-6 det-info"] span[class="antes"]')) else None
    description = html_page.find('.det-des p', first=True).text if html_page.find('.det-des p', first=True) else None
    brand = html_page.find('div[class="info-middle mb-2"] .active', first=True).text if html_page.find(
        'div[class="info-middle mb-2"] .active', first=True) else None
    product_url = html_page.url

    product = Product(
        Product_Name=name,
        Brand=brand,
        Category_Name=category_name,
        Current_Price=current_price,
        Actual_Price=actual_price,
        Description=description,
        Product_URL=product_url,
        Category_URL=category_url,
    )

    insert_to_database(product)


def export_to_file() -> None:
    """
    Exporting database to excel
    :return: None
    """

    df = pandas.read_sql_table('Product_Information', con=engine)
    df.to_excel('Products of super selectos.xlsx', index=False, engine='openpyxl')
    df.to_csv(r'D:\Github\aprinur\superselectos.com\Products of super selectos.csv', index=False)
    print('Result saved as Products of super selectos')


def load_proceed_urls():
    if not os.path.exists(PROGRESS_FILE):
        return set()
    with open(PROGRESS_FILE, 'r') as file:
        return set(line.strip() for line in file)


def save_proceed_url(url):
    with open(PROGRESS_FILE, 'a') as file:
        file.write(url + '\n')
