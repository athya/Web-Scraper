import psycopg2
import password as ps

#GET num amount of urls from database that have no movie data associated with them
def getEmptyURLS(num):
    con = psycopg2.connect("dbname='scraper' user='postgres' host='localhost' password='" + ps.password + "'")
    cursor = con.cursor()

    cursor.execute("SELECT url FROM movie WHERE (title is null or title = '') LIMIT " + str(num) + ";")

    urls = []
    for row in cursor:
        urls.append(str(row)[2:len(row)-4]) #remove quotes

    print(urls)
    return urls

def getMovieData(name):
    return
    #get movie data by name
    #to-do

def updateMovieData(filename):
    con = psycopg2.connect("dbname='scraper' user='postgres' host='localhost' password='" + ps.password + "'")
    cursor = con.cursor()

    url = "https://www.metacritic.com/movie/the-workshop"
    #need to close??

    with open(filename, 'r') as infile:
        cursor.execute("DELETE FROM movie WHERE (url = '" + url + "');");
        #hacky?
        cursor.copy_from(infile, 'movie', sep='|', columns=("url","title","release_date","summary"))
        con.commit()
    #do something
    return

updateMovieData("The Workshop.csv")
