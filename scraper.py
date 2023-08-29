import csv
import requests
from bs4 import BeautifulSoup

section_urls = [
    'https://www.castelli-cycling.com/FR/fr/Homme/c/Man?q=%3Arelevance&page=',
    'https://www.castelli-cycling.com/FR/fr/Femme/c/Woman?q=%3Arelevance&page='
]

products_per_page = 25

def extract_field(soup, selector, attribute=None, default=None):
    try:
        if attribute:
            return soup.select_one(selector)[attribute]
        else:
            return soup.select_one(selector).text.strip()
    except (AttributeError, KeyError):
        return default

def get_product_data(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    products = soup.find_all('div', class_='col-sm-6 col-md-4 mb-3 product-item')

    for product in products:
        product_data = {}

        title = extract_field(product, 'p.m-0.h5.text-center.slideTitle', default=None)
        price = extract_field(product, 'span.f500.price-span', default=None)
        compared_price = extract_field(product, 'span.sconto', default=None)
        img_link = extract_field(product, 'img', 'src', default=None)

        product_link = product.find('a')['href']
        product_page = requests.get(product_link).text
        product_soup = BeautifulSoup(product_page, 'lxml')

        description = extract_field(product_soup, 'p.text-left.shortdesc.h5.f300', default=None)
        type = extract_field(product_soup, 'ol.breadcrumb li:last-child a', default=None)

        size_inputs = product_soup.find_all('input', class_='form-check-input')
        size_values = [size_input['value'] for size_input in size_inputs if 'value' in size_input.attrs]
        size = ', '.join(size_values)

        weight = extract_field(product_soup, 'span.char-value', default=None)

        product_data['Handle'] = title.lower().replace(' ', '-') if title else None
        product_data['Title'] = title
        product_data['Body (HTML)'] = description
        product_data['Vendor'] = 'Castelli'
        product_data['Type'] = type
        product_data['Tags'] = ' '.join(title.split()) if title else None
        product_data['Published'] = 'TRUE'
        product_data['Option1 Name'] = 'Size'
        product_data['Option1 Value'] = size
        product_data['Variant SKU'] = f'{title.lower().replace(" ", "-")}-m' if title else None
        product_data['Variant Grams'] = weight
        product_data['Variant Inventory Tracker'] = 'deny'
        product_data['Variant Inventory Qty'] = '25'
        product_data['Variant Inventory Policy'] = 'manual'
        product_data['Variant Fulfillment Service'] = ''
        product_data['Variant Price'] = price
        product_data['Variant Compare At Price'] = compared_price
        product_data['Variant Requires Shipping'] = 'TRUE'
        product_data['Variant Taxable'] = 'TRUE'
        product_data['Image Src'] = img_link
        product_data['Image Alt Text'] = f'{title} Image' if title else None
        product_data['Variant Image'] = img_link
        print(f'Product {title} recorded')
        yield product_data

product_data = []

for section_url in section_urls:
    page_number = 1
    while True:
        url = f'{section_url}{page_number}'
        try:
            products = list(get_product_data(url))

            if not products:
                break

            product_data.extend(products)
            page_number += 1
        except Exception as e:
            print(f"An error occurred: {e}")

# Write the product data to a CSV file
with open('products.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = product_data[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(product_data)

print("Scraping and CSV creation completed successfully.")