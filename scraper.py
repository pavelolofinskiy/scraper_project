
from bs4 import BeautifulSoup
import requests
product_url = 'https://www.castelli-cycling.com/FR/fr/Homme/c/Man?q=%3Arelevance&page=19'

# Get the page content
html_text = requests.get(product_url).text
soup = BeautifulSoup(html_text, 'lxml')
# Find the product information on the page
product = soup.find('div', class_='col-sm-6 col-md-4 mb-3 product-item')

# Extract product details
title = product.select_one('p.m-0.h5.text-center.slideTitle').text.strip()
price = product.select_one('span.f500.price-span').text.strip()
compared_price = product.select_one('span.sconto')
if compared_price:
    # Extract the compared price from the element
    compared_price = compared_price.text.strip()
else:
    # Set a default value (e.g., 'N/A' or an empty string) if the element does not exist
    compared_price = 'None'
description = product.select_one('p.m-0.text-center').text.strip()
img_link = product.find('img')['src']

product_link = product.find('a')['href']
product_page = requests.get(product_link).text
product_soup = BeautifulSoup(product_page, 'lxml')

type_soup = product_soup.select('ol.breadcrumb li')

type_list = []
found_type = False

for value in type_soup:
    if found_type:
        break

    if value.a:
        category = value.a.text.strip()
        type_list.append(category)
    else:
        found_type = True
type = type_list[-1]


size_inputs = product_soup.find_all('input', class_='form-check-input')
size_values = [size_input['value'] for size_input in size_inputs if 'value' in size_input.attrs]
size = ', '.join(size_values)

weight = product_soup.select_one('span.char-value').text.strip()

print(f'Title: {title}')
print(f'Price: {price}')
print(f'Weight: {weight}')
print(f'Type: {type}')
print(f'Size: {size}')
print(f'comp Price: {compared_price}')
print(f'Description: {description}')
print(f'Image Link: {img_link}')