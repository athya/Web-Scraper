#import numpy as np
#import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
import csv

#storing html of page in result variable
#maybe work on scraping dynamic websites later
#consider using Xpath rather than CSS selector
#consider watching for server side blacklisting by using proxies
#add (random?) wait times
#maybe work on captchas later
#abstract away!
def scrapeMovieInfo(url):
    #to prevent being blocked
    my_session = requests.session()
    for_cookies = my_session.get("https://www.metacritic.com")
    cookies = for_cookies.cookies
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    my_url = url

    response = my_session.get(my_url, headers=headers, cookies=cookies)
    print(response.status_code)  # 200
    
    page = response.text #get HTML from URL

    soup = BeautifulSoup(page,'html.parser') #parses html
    title_text = soup.find('h1').text
    release_date = soup.find('span', class_='release_year lighter').text
    summary = soup.find('div',class_='summary_deck details_section')
    summary_text = summary.find('span', class_='blurb blurb_expanded').text

    reviews = soup.find_all('a', {'id': 'nav_to_metascore'}, href=True) #not working
    print(reviews);
    links = [];
    for review in reviews:
         ref = review['href']
         links.append(ref)
    
    web_data = {
        'title': title_text,
        'release date': release_date,
        'summary': summary_text,
        'review links': links
    }
    
    with open('movieData.txt', 'w') as outfile: #better syntax and exception handling, will automatically close file
#json.dump(web_data, outfile) #format data as json and write to outfile
        writer = csv.writer(outfile)
        writer.writerows(web_data)

def scrapeMovieLinks(url):
    my_session = requests.session()
    for_cookies = my_session.get("https://www.metacritic.com")
    cookies = for_cookies.cookies
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    my_url = url

    response = my_session.get(my_url, headers=headers, cookies=cookies)
    print(response.status_code)  # 200

    page = response.text #get XML from URL
    soup = BeautifulSoup(page, 'xml') #parses XML
    valid_movies = []
    links = soup.find_all('loc')
    for link in links:
        content = link.text
        index = content.find("movie/")
        if index != -1 and (index + 6) <= len(content) and content[index+6:].find("/") == -1:
            valid_movies.append(content)

    with open('movieLinks.csv', 'a+') as outfile: #better syntax and exception handling, will automatically close file
        writer = csv.writer(outfile)
        for line in valid_movies:
            writer.writerow([line])

def initializeMovieList():
    scrapeMovieLinks('https://www.metacritic.com/sitemap/Movie-movie/1/sitemap.xml')
    scrapeMovieLinks('https://www.metacritic.com/sitemap/Movie-movie/2/sitemap.xml')
    scrapeMovieLinks('https://www.metacritic.com/sitemap/Movie-movie/3/sitemap.xml')

initializeMovieList()
    
#scrapeMovieInfo('https://www.metacritic.com/movie/joker?ref=hp')
