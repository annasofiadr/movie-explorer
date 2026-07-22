import requests

API_KEY = "de733008236246d973c4bc6ad48dfd86"

url = "https://api.themoviedb.org/3/search/movie"

params = {
    "api_key": API_KEY,
    "query": "Batman"
}

response = requests.get(url, params=params)

data = response.json()

print(data)