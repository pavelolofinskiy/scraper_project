from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.castelli-cycling.com/FR/fr/Homme/Cyclisme/Top/Maillots-de-cyclisme-pour-hommes/c/Man-Cyc-Top-Jer').text
soup = BeautifulSoup(html_text, 'lxml')
products = soup.find_all('div', class_ = 'col-sm-6 col-md-4 mb-3 product-item')
for product in products:
    price = product.find('span', class_ = 'f500 price-span').text
    description = product.find('p', class_ = 'm-0 text-center').text
    img_link = product.find('img')['src']
    print(f'''
    Product Price: {price}
    Product Description: {description} 
    Image Link: {img_link}
    ''')


