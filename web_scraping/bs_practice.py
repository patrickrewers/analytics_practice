from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime

# Provide URL to select data from
url = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38'

# Opening up connection and downloading content
uClient = uReq(url)
page_html = uClient.read()
uClient.close()

# HTML parsing
page_soup = soup(page_html, 'html.parser')

# Find all divs related to graphics cards
containers = page_soup.findAll('div', {'class': 'item-container'})

# Print out how many products there are on this page
print('Found', len(containers), 'products on this page.')

# Extract information from each product
products = []
for container in containers:
    product = {}
    product['brand'] = container.a.next_sibling.next_sibling.div.a.img['title']
    product['title'] = container.findAll('a', {'class': 'item-title'})[0].get_text()
    try:
        product['rating'] = container.findAll('a', {'class': 'item-rating'})[0]['title'][-1]
    except:
        pass
    product['price'] = container.findAll('span', {'class': 'price-current-label'})[0].next_sibling.next_sibling.get_text()
    product['shipping'] = container.findAll('li', {'class': 'price-ship'})[0].get_text().strip()
    products.append(product.copy())

# Convert list of products to DataFrame
df = pd.DataFrame(products)

# Export DataFrame as CSV
title = 'products_' + str(datetime.datetime.today().strftime('%m_%d_%Y_%X'))+'.csv'
df.to_csv(title, index=False)
