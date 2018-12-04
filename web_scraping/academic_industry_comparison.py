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

# Downloads text groups from websites, and removes introduction to leave only articles
articles = oreilly_soup.findAll('div', {'class': 'text-group'})
articles = articles[1:]

# Loop through articles, and store title, deck, and url for each article in dictionary format
#   At the end of each loop, append a copy of the dictionary to a list
article_list = []
for article in articles:
    article_dictionary = {}
    article_dictionary['title'] = article.a.get_text()
    article_dictionary['deck'] = article.p.get_text()
    article_dictionary['url'] = 'https://www.oreilly.com' + article.a['href']
    article_list.append(article_dictionary)
