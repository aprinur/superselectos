from bs4 import BeautifulSoup
import time
from requests_html import HTMLSession


from playwright.sync_api import sync_playwright

BASE_URL = "https://www.superselectos.com/"

def get_category_link(main_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(main_url, wait_until='domcontentloaded')
        while True:
            if 'rz-dialog rz-modal-image-viewer rz-modal-centered' in page.content():
                add_exit(page)
                continue
            break

        page.locator('a[class="nav-link nav-link-all"]').click()

        categories = [cat.text_content() for cat in page.query_selector_all('.cat-level-content')]
        categories = [i.strip() for i in categories[0].split("\n")]
        for i in categories:
            ...

        # print(page.content())
        time.sleep(10)


def add_exit(page):
    page.locator('a[class="rz-dialog-titlebar-icon rz-dialog-titlebar-close"]').click()


def get_product_url(category):
    session = HTMLSession()

    response = session.get(category)

    product_url = list([i.absolute_links for i in response.html.find('.right-content')][0])
    product_url = [product_url.remove(i) for i in product_url if 'Id' not in i]
    
    print(product_url)
    


def get_html_product(url):
    session = HTMLSession()

    response = session.get(url)
    html = response.html
    print(html)

    return html


def product_parser(html_page):    
    name = html_page.find('h1[class="det-nom"]', first=True).text
    current_price = html_page.find('div[class="info-middle mb-2"] div[class="right"]', first=True).text
    actual_price = html_page.find('div[class="col-md-6 det-info"] span[class="antes"]')
    description = html_page.find('.det-des p', first=True).text
    brand = html_page.find('div[class="info-middle mb-2"] .active', first=True).text if html_page.find('div[class="info-middle mb-2"] .active', first=True) else None
    product_url = html_page.url

    return{
        "Name": name,
        "Current Price": current_price,
        "Actual Price": actual_price,
        'Description': description,
        'Brand': brand,
        'Product_URL': product_url,
        # 'Category_URL': category_url
    }


def main(url):
    # product_page = get_html_product(url)
    # print(product_parser(product_page))
    # get_category_link(url)
    get_product_url(url)
    ...

if __name__ == "__main__":
    main("https://www.superselectos.com/products?category=0114")