#import numpy as np
#import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
import csv
import time

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

def getMovieInfo(url, HTML):
    soup = BeautifulSoup(HTML,'html.parser')
    
    title_text = soup.find('h1').text
    release_date = soup.find('span', class_='release_year lighter').text
    
    summary = soup.find('div',class_='summary_deck details_section')
    summary_text = ''
    if summary is not None: #put more error checks! abstract away
        summary_text = summary.text
        summary_chunk = (summary.find_all('span'))[1].find('span')
        if summary_chunk is not None:
            summary_text = summary_chunk.text
        summary_chunk = summary.find('span', class_='blurb blurb_expanded')
        if summary_chunk is not None:
            summary_text = summary_chunk.text
    
    try:
        metascore = soup.find('a', class_="metascore_anchor").find('span').text
    except:
        metascore = ""

    try:
        director = soup.find('div', class_='director').find('a').text
    except:
        director = ""

    try:
        genres = soup.find('div',class_='genres').find_all('span')[1].text.strip()
        genres = "".join(genres.split())
    except:
        genres = ""

    try:
        rating = soup.find('div',class_='rating').find_all('span')[1].text.strip()
    except:
        rating = ""

    actors = []
    try:
        actors_html = soup.find('div', class_='summary_cast details_section').find_all('a')
        for actor in actors_html:
            name = actor.text
            actors.append(name)
    except:
        actors = []
        #do nothing

    try:
        distributer = soup.find('div', class_='details_section').find('a').text
    except:
        distributer = ''

    reviews = soup.find_all('div', class_="summary")
    links = []
    for review in reviews:
        tagged_link = review.find("a")
        #print(review)
        #print(tagged_link)
        if tagged_link is not None:
            link_content = tagged_link['href']
            if "http" in link_content:
                links.append(link_content)
    
    web_data = {
        'url': url,
        'title': title_text,
        'director': director,
        'distributer': distributer,
        'release_date': release_date,
        'genres': genres,
        'rating': rating,
        'metascore': metascore,
        'summary': summary_text,
        'actors': actors,
        'review_links': links
    }
    
    return web_data

def scrapeMovieInfo(url):
    html = getHTML(url)
    result = getMovieInfo(url, html)
    return result

scrapeMovieInfo('https://www.metacritic.com/movie/hustlers')

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

    time.sleep(15)

def initializeMovieList():
    scrapeMovieLinks('https://www.metacritic.com/sitemap/Movie-movie/1/sitemap.xml')
    scrapeMovieLinks('https://www.metacritic.com/sitemap/Movie-movie/2/sitemap.xml')
    scrapeMovieLinks('https://www.metacritic.com/sitemap/Movie-movie/3/sitemap.xml')

def movieToFile(urls):
    if not isinstance(urls, list):
        #add error statement? #add better error handling
        return

    for url in urls:
        web_data = scrapeMovieInfo(url)
        print(url)
        print(web_data)
        #with open(web_data.get('title') + '.csv', 'w+') as outfile:
            #writer = csv.DictWriter(outfile, fieldnames=list(web_data.keys()), delimiter = '|')
            #writer.writerow(web_data)

#make some kind of global table labels thing?
