import api
import webscraper as ws

urls = api.getEmptyURLS(10)
ws.movieToFile(urls)

