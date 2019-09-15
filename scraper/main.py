import api
import webscraper as ws

urls = api.getEmptyURLS(100)
print(urls)
ws.movieToFile(urls)

