from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

oreilly_url = 'https://www.oreilly.com/topics/data-science'
jds_url = 'http://www.jds-online.com/'

# Opening up connection and downloading content
uClient = uReq(oreilly_url)
oreilly_html = uClient.read()
uClient = uReq(jds_url)
jds_html = uClient.read()
uClient.close()

# HTML parsing
oreilly_soup = soup(oreilly_html, 'html.parser')
jds_soup = soup(jds_html, 'html.parser')

# Print off first paragraph tag of each site
print(oreilly_soup.body.p)
print(jds_soup.body.p)