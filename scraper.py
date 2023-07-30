import csv
from bs4 import BeautifulSoup
import requests

section_urls = [
    'https://www.castelli-cycling.com/FR/fr/Homme/c/Man?q=%3Arelevance&page=',
    'https://www.castelli-cycling.com/FR/fr/Femme/c/Woman?q=%3Arelevance&page='
]

products_per_page = 25

def get_product_data(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    products = soup.find_all('div', class_='col-sm-6 col-md-4 mb-3 product-item')

    for product in products:
        title = product.select_one('p.m-0.h5.text-center.slideTitle').text
        price = product.select_one('span.f500.price-span').text
        compared_price = product.select_one('span.sconto')
        compared_price = compared_price.text.strip() if compared_price else 'None'
        img_link = product.find('img')['src']

        product_link = product.find('a')['href']
        product_page = requests.get(product_link).text
        product_soup = BeautifulSoup(product_page, 'lxml')

        description_element = product_soup.find('p', class_='text-left shortdesc h5 f300')
        description = description_element.text.strip() if description_element else 'None'

        type_soup = product_soup.select('ol.breadcrumb li')
        category_list = [value.a.text.strip() for value in type_soup if value.a]
        type = category_list[-1]

        size_inputs = product_soup.find_all('input', class_='form-check-input')
        size_values = [size_input['value'] for size_input in size_inputs if 'value' in size_input.attrs]
        size = ', '.join(size_values)

        weight = product_soup.select_one('span.char-value').text.strip()

        yield {
            'Handle': title.lower().replace(' ', '-'),
            'Title': title,
            'Body (HTML)': description,
            'Vendor': 'Castelli',
            'Type': type,
            'Tags': ' '.join(title.split()),
            'Published': 'TRUE',
            'Option1 Name': 'Size',
            'Option1 Value': size,
            'Variant SKU': f'{title.lower().replace(" ", "-")}-m',
            'Variant Grams': weight,
            'Variant Inventory Tracker': 'deny',
            'Variant Inventory Qty': '25',
            'Variant Inventory Policy': 'manual',
            'Variant Fulfillment Service': '',
            'Variant Price': price,
            'Variant Compare At Price': compared_price,
            'Variant Requires Shipping': 'TRUE',
            'Variant Taxable': 'TRUE',
            'Image Src': img_link,
            'Image Alt Text': f'{title} Image',
            'Variant Image': img_link
        }

product_data = []

for section_url in section_urls:
    page_number = 1
    while True:
        url = f'{section_url}{page_number}'
        products = list(get_product_data(url))

        if not products:
            break

        product_data.extend(products)
        page_number += 1

# Write the product data to a CSV file
with open('products.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = product_data[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(product_data)

print("Scraping and CSV creation completed successfully.")