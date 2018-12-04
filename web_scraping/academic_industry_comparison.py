from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd


# Open up connection and download content
def download(url):
    uClient = uReq(url)
    html = uClient.read()
    uClient.close()
    return html


def o_reilly_scraper():
    # Scrape article title, deck, and url from O'Reilly Media's data science topic page, and export
    html = download('https://www.oreilly.com/topics/data-science')
    html_soul = soup(html, 'html.parser')
    # Extract text groups from html, and remove introduction to leave only articles
    articles = html_soul.findAll('div', {'class': 'text-group'})
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
    # Convert the article list to a DataFrame, in order to easily aggregate and analyze data later
    return pd.DataFrame(article_list)


def jds_scraper():
    # Scrape journal title,
    html = download('http://www.jds-online.com/')
    html_soul = soup(html, 'html.parser')
    return
