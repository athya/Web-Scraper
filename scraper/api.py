import psycopg2
import password as ps

#GET num amount of urls from database that have no movie data associated with them
def getEmptyURLS(num):
    con = psycopg2.connect("dbname='scraper' user='postgres' host='localhost' password='" + ps.password + "'")

    print(con)

    cursor = con.cursor()
    cursor.execute("SELECT url FROM movie WHERE (movie_title is null or movie_title = '') LIMIT " + str(num) + ";")

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
    #do something
    return

getEmptyURLS(2)
