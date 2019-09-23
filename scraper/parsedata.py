import time
from bs4 import BeautifulSoup
import csv
import os

keys = [
            'url',
            'title',
            'director',
            'distributer',
            'release_date',
            'genres',
            'rating',
            'metascore',
            'summary',
            'actors',
            'reviews'
        ]

def movieToFile(movie_data):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = './data/' + timestr + '.csv'
    with open(filename, 'w+') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=list(movie_data.keys()), delimiter = '|')
        writer.writerow(movie_data)
        return filename

def fileToMovie(file, keys):
    with open (file, 'r') as infile:
        reader = csv.DictReader(infile, fieldnames=keys, delimiter = '|')
        mydict = {rows[0]:rows[1] for rows in reader}
#given an HTML file with the url as the first line of the file, get
#movie data
def getMovieInfo(file):
    with open (file, 'r') as infile:
        url = infile.readline().strip()
        soup = BeautifulSoup(infile.read(),'html.parser')
        
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
            'reviews': links
        }

        print(web_data)
        return web_data

#get num number of files from the folder at path
def getFiles(path, num):
    #r is root, d is directories, f is files
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))

    return files

#delete file given full filename
def deleteFile(file):
    if os.path.exists(file):
        os.remove(file)
    else:
        print("The file does not exist") #handle errors better
