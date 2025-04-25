import datetime
import time

from src import get_category_url, get_product_url, get_html_product, get_all_page, check_page, product_parser, \
    export_to_file, BASE_URL, load_proceed_urls, save_proceed_url


def main(main_url):
    start = time.time()
    time_start = datetime.datetime.now()
    while True:
        try:

            proceed = load_proceed_urls()
            categories = get_category_url(main_url)

            for category_name, category_url in categories.items():
                print(f'Opening category {category_name}: {category_url}')
                if check_page(category_url):
                    pagination = get_all_page(category_url)

                    for page in pagination:
                        new_url = f'{category_url}&page={page}'
                        product_urls = get_product_url(new_url)
                        print(f'Opening page {new_url}')

                        for product in product_urls:
                            if product in proceed:
                                continue
                            html = get_html_product(product)
                            product_parser(html, category_name=category_name, category_url=category_url)
                            print(f'Parsing product: {product}')
                            save_proceed_url(product)

                product_urls = get_product_url(category_url)
                for product in product_urls:
                    if product in proceed:
                        continue
                    html = get_html_product(product)
                    product_parser(html, category_name=category_name, category_url=category_url)
                    print(f'Parsing product: {product}')
                    save_proceed_url(product)

            export_to_file()

            break
        except Exception:
            print(f'Internet connection error ')
            time.sleep(5)

    finish = time.time()
    finish_time = datetime.datetime.now()
    print(f'Total running time: {(finish - start) / 3600:.2f} Hours')
    print(f'Start program {time_start} ')
    print(f'Finish program {finish_time} ')


if __name__ == "__main__":
    main(BASE_URL)
