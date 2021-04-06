import psycopg2

#NOTE: $ brew install unixodbc solved import error!

#get urls from database that have no movie data associated with them
def getEmptyURLS():
    con = psycopg2.connect("dbname='scraper' user='postgres' host='localhost' password='Ironer38'")

    print(con)

    cursor = con.cursor()
    cursor.execute("SELECT url FROM movie WHERE (movie_title is null or movie_title = '') LIMIT 10;")

    urls = []
    for row in cursor:
        urls.append(str(row)[2:len(row)-4]) #remove quotes

    print(urls)
    return urls

getURLS()
