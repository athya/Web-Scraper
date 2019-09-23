import api
import webscraper as ws
import parsedata as pd

#make global
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

num = 5
urls = api.getEmptyURLS(num) # get urls from database
for url in urls:
    api.removeURL(url) #remove them from the database
print(urls)
for url in urls: #get html and put in file form
    html = ws.getHTML(url)
    ws.HTMLtoFile(url, html)
path = './html'
files = pd.getFiles(path, num)
for file in files:
    web_data = pd.getMovieInfo(file)
    pd.movieToFile(web_data)
    pd.deleteFile(file)
path = './data'
files = pd.getFiles(path, num)
for file in files:
    data = pd.fileToMovie(file, keys) # don't know if this method works...
    api.addMovieData(data)
    pd.deleteFile(file)

print("DONE!")

