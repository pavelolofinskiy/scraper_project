from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.castelli-cycling.com/FR/fr/Homme/Cyclisme/Top/Maillots-de-cyclisme-pour-hommes/c/Man-Cyc-Top-Jer').text
soup = BeautifulSoup(html_text, 'lxml')
products = soup.find_all('div', class_='col-sm-6 col-md-4 mb-3 product-item')

for product in products:
    title = product.select_one('p.m-0.h5.text-center.slideTitle').text
    price = product.select_one('span.f500.price-span').text
    description = product.select_one('p.m-0.text-center').text.strip()
    img_link = product.find('img')['src']

    product_link = product.find('a')['href']
    product_page = requests.get(product_link).text
    product_soup = BeautifulSoup(product_page, 'lxml')
    weight = product_soup.select_one('span.char-value').text
    
    print(f'''
    Title: {title}
    Price: {price}
    Weight: {weight}
    Description: {description}
    Image Link: {img_link}
    ''')

