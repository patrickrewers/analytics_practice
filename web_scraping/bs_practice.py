from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

url = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38'
print(url)

# Opening up connection and downloading content
uClient = uReq(url)
page_html = uClient.read()
uClient.close()

# HTML parsing
page_soup = soup(page_html, 'html.parser')
print(page_soup.h1)
