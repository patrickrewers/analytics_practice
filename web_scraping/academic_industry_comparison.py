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
    html_soup = soup(html, 'html.parser')
    # Extract text groups from html, and remove introduction to leave only articles
    print('Connection established. Extracting article information...')
    articles = html_soup.findAll('div', {'class': 'text-group'})
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
    # Return list of article information
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

def kdnuggets_topic_scraper():
    # Scrape article title and deck from KDnuggets news page
    print('Establishing connection with kdnuggets.com...')
    html = download('https://www.kdnuggets.com/news/index.html')
    html_soup = soup(html, 'html.parser')
    # Extract article information in list form from the soup
    print('Connection established. Extracting article information...')
    raw_titles = html_soup.findAll('ul', {'class': 'three_ul'})[0].findAll('b')
    raw_urls = html_soup.findAll('ul', {'class': 'three_ul'})[0].findAll('a', {'rel': False})
    raw_decks = html_soup.findAll('ul', {'class': 'three_ul'})[0].findAll('div')
    raw_dates = html_soup.findAll('ul', {'class': 'three_ul'})[0].findAll('font')
    # Iterate through each article and save it's extracted info to a list as a dictionary
    article_list = []
    for i, title in enumerate(raw_titles, 0):
        article = {}
        article['title'] = title.get_text()
        article['url'] = raw_urls[i].get('href')
        article['deck'] = raw_decks[i].get_text()
        article['date'] = raw_dates[i].get_text()[2:-1]
        article_list.append(article)
    return article_list


def kdnuggets_copy_scraper(article):
    # Scrape author, publication date, and copy for each O'Reilly article provided
    html = download(article['url'])
    html_soup = soup(html, 'html.parser')
    html_copy = html_soup.findAll('span', {'style': True})
    cleaned_copy = ''
    for tag in html_copy:
        cleaned_copy += tag.get_text().replace(',', '') + ('\n')
    article['copy'] = cleaned_copy
    return article


def scraper():
    # Scrapes data from O'Reilly Media
    print("\nCollecting article titles from O'Reilly Media.")
    oreilly_article_list = oreilly_topic_scraper()
    print('\n{} articles found. Scraping articles.'.format(len(oreilly_article_list)))
    for i in tqdm(range(len(oreilly_article_list))):
        oreilly_article_list[i] = oreilly_copy_scraper(oreilly_article_list[i])
    # Scrapes data from KDnuggets
    print("\nCollecting article titles from KDnuggets.")
    kdnuggets_article_list = kdnuggets_topic_scraper()
    print('\n{} articles found.'.format(len(kdnuggets_article_list)))
    for i in tqdm(range(len(kdnuggets_article_list))):
        kdnuggets_article_list[i] = kdnuggets_copy_scraper(kdnuggets_article_list[i])
    # Print a line to separate sections
    print('')
    return oreilly_article_list, kdnuggets_article_list


def aggregator(oreilly_article_list, kdnuggets_article_list):
    # Convert newly added data to DataFrame
    new_data = pd.DataFrame(oreilly_article_list)
    # Attempt to merge with old data. Otherwise, create new CSV file
    try:
        old_data = pd.read_csv('oreilly.csv')
        print('Previous data found. Adding any new articles...')
        data = pd.concat([old_data, new_data])
        data.drop_duplicates(subset=['url'], inplace=True)
        data.to_csv('oreilly.csv', index=False)
        print('Aggregation complete\n')
    except FileNotFoundError:
        print("No previous O'Reilly data found. Creating new CSV file named 'oreilly.csv\n")
        new_data.to_csv('oreilly.csv', index=False)
    print('')


def main():
    # Provide command options and await input
    print("Options: -r: Refresh data\t-a: Aggregate data\t-q: Quit\n")
    while True:
        choice = input("Input: ")
        # Quit program using the 'q' command
        if(choice == '-q'):
            break
        # Re-print options if user types 'help'
        elif(choice == 'help'):
            print("Options: -r: Refresh data\t-a: Aggregate data\t-q: Quit\n")
        # Scrape articles with the 'r' command
        elif(choice == '-r'):
            oreilly_article_list, kdnuggets_article_list = scraper()
        # Aggregate articles with the 'a' command
        elif(choice == '-a'):
            try:
                aggregator(oreilly_article_list, kdnuggets_article_list)
            except UnboundLocalError:
                print("No data to aggregate. Use -r to scrape the most recent data.\n")
        else:
            print("Not a valid input. Enter 'help' for commands")


main()
