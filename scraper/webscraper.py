import requests
import json
from bs4 import BeautifulSoup
import csv
import time
import random
#maybe work on scraping dynamic websites later
#consider using Xpath rather than CSS selector
#consider watching for server side blacklisting by using proxies
#add (random?) wait times
#maybe work on captchas later

def getHTML(url):
    my_session = requests.session()
    for_cookies = my_session.get("https://www.metacritic.com")
    cookies = for_cookies.cookies
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    my_url = url
    
    response = my_session.get(my_url, headers=headers, cookies=cookies)
    print(response.status_code)  # 200
    
    page = response.text #get HTML from URL

    return page

def HTMLtoFile(url, HTML):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    with open ('./html/' + timestr + '.html', 'w+') as outfile:
        outfile.write(url + '\n')
        outfile.write(html)

url = 'https://www.metacritic.com/movie/hustlers'
html = getHTML(url)
HTMLtoFile(url, html)

#scrapes metacritic links to movies given a link to an xml sitemap
def scrapeMovieLinks(url):
    my_session = requests.session()
    for_cookies = my_session.get("https://www.metacritic.com")
    cookies = for_cookies.cookies
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    my_url = url

    response = my_session.get(my_url, headers=headers, cookies=cookies)
    print(response.status_code)

    page = response.text #get XML from URL
    soup = BeautifulSoup(page, 'xml') #parses XML
    valid_movies = []
    links = soup.find_all('loc')
    for link in links:
        content = link.text
        index = content.find("movie/")
        if index != -1 and (index + 6) <= len(content) and content[index+6:].find("/") == -1:
            valid_movies.append(content)

    with open('movieLinks.csv', 'a+') as outfile: 
        writer = csv.writer(outfile)
        for line in valid_movies:
            writer.writerow([line])

    time.sleep(5)

#scrapes all movie links from metacritic
def initializeMovieList():
    scrapeMovieLinks('https://www.metacritic.com/sitemap/Movie-movie/1/sitemap.xml')
    scrapeMovieLinks('https://www.metacritic.com/sitemap/Movie-movie/2/sitemap.xml')
    scrapeMovieLinks('https://www.metacritic.com/sitemap/Movie-movie/3/sitemap.xml')


#make some kind of global table labels thing?

