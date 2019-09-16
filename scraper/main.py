import api
import webscraper as ws
import parsedata as pd

urls = api.getEmptyURLS(100)
for url in urls:
    pd.removeURL(url)
print(urls)
ws.movieToFile(urls)

