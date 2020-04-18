import requests

url = requests.get("https://www.australvaldivia.cl/impresa/2020/03/13/papel/")

print(url.content)