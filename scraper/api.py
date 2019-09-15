import psycopg2
import webscraper as ws
import password as ps

#GET num amount of urls from database that have no movie data associated with them
def getEmptyURLS(num):
    con = psycopg2.connect("dbname='scraper' user='postgres' host='localhost' password='" + ps.password + "'")
    cursor = con.cursor()

    cursor.execute("SELECT url FROM unscraped_url LIMIT " + str(num) + ";")

    urls = []
    for row in cursor:
        urls.append(str(row)[2:len(row)-4]) #remove quotes

    return urls

def getMovieData(name):
    return
    #get movie data by name
    #to-do

def addMovieData(movie_data):
    con = psycopg2.connect("dbname='scraper' user='postgres' host='localhost' password='" + ps.password + "'")
    cursor = con.cursor()

    #need to close??
    
    #ws.scrapeMovieInfo(url)
    with open('temp.csv', 'w+') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=list(movie_data.keys()), delimiter = '|')
        writer.writerow(web_data)

    with open(filename, 'r') as infile:
        cursor.execute("DELETE FROM unscraped_url WHERE (url = '" + url + "');");
        cursor.copy_from(infile, 'movie', sep='|', columns=("url","title","release_date","summary"))
        con.commit()

#addMovieData("The Workshop.csv")
