from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from tqdm import tqdm
import pandas as pd

# Open up connection and download content
def download(url):
    uClient = uReq(url)
    html = uClient.read()
    uClient.close()
    return html


def oreilly_topic_scraper():
    # Scrape article title, deck, and url from O'Reilly Media's data science topic page, and export
    print('Establishing connection with oreilly.com...')
    html = download('https://www.oreilly.com/topics/data-science')
    html_soul = soup(html, 'html.parser')
    # Extract text groups from html, and remove introduction to leave only articles
    print('Connection established. Extracting article information...')
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
    print('Information extracted.')
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
    print("\nCollecting article titles from O'Reilly Media.")
    article_list = oreilly_topic_scraper()
    print('\n{} articles found. Scraping articles.'.format(len(article_list)))
    for i in tqdm(range(len(article_list))):
        article_list[i] = oreilly_copy_scraper(article_list[i])
    print('')
    return article_list


def aggregator(article_list):
    new_data = pd.DataFrame(article_list)
    try:
        old_data = pd.read_csv('oreilly.csv')
        print('Previous data found. Adding any new articles...')
        data = pd.concat([old_data, new_data])
        data.drop_duplicates(subset=['url'], inplace=True)
        data.to_csv('oreilly.csv', index=False)
        print('Aggregation complete\n')
    except FileNotFoundError:
        print("No previous data found. Creating new CSV file named 'oreilly.csv\n")
        new_data.to_csv('oreilly.csv', index=False)
    print('')


def main():
    print("Options: -o: Add data from O'Reilly\t-a: Aggregate data\t-q: Quit\n")
    while True:
        choice = input("Input: ")
        if(choice == '-q'):
            break
        elif(choice == 'help'):
            print("Options: -o: Add data from O'Reilly\t-a: Aggregate data\t-q: Quit\n")
        elif(choice == '-o'):
            article_list = scraper()
        elif(choice == '-a'):
            try:
                aggregator(article_list)
            except UnboundLocalError:
                print("No data to aggregate. Use -o to get data from O'Reilly media first.\n")


main()