from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


# Open up connection and download content
def download(url):
    uClient = uReq(url)
    html = uClient.read()
    uClient.close()
    return html


def oreilly_topic_scraper():
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
        article_dictionary['title'] = article.a.get_text().replace(',', '')
        article_dictionary['deck'] = article.p.get_text().replace(',', '')
        article_dictionary['url'] = 'https://www.oreilly.com' + article.a['href']
        article_list.append(article_dictionary)
    # Convert the article list to a DataFrame, in order to easily aggregate and analyze data later
    return article_list


def oreilly_copy_scraper(article):
    # Scrape author, publication date, and copy for each O'Reilly article provided
    html = download(article['url'])
    html_soup = soup(html, 'html.parser')
    article['author'] = html_soup.findAll('span', {'class': 'author'})[0].a.get_text().replace(',', '')
    article['date'] = html_soup.findAll('time', {'class': 'date'})[0].get_text().replace(',', '')
    html_copy = html_soup.findAll('div', {'class': 'article-body'})[0].findAll({'p': True})[1:]
    cleaned_copy = ''
    for tag in html_copy:
        cleaned_copy += tag.get_text().replace(',', '') + ('\n')
    article['copy'] = cleaned_copy
    return article



def scraper():
    # Scrapes data from leading Data Science publications and compares them
    article_list = oreilly_topic_scraper()
    for article in article_list:
        article = oreilly_copy_scraper(article)
    return article_list