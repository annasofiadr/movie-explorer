import requests
import os


API_KEY = os.environ["TMDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"
REQUEST_TIMEOUT = 10


def search_movies(query):
    if not query or not query.strip():
        return []

    url = f"{BASE_URL}/search/movie"

    params = {
        "api_key": API_KEY,
        "query": query.strip(),
        "include_adult": "false"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()
        return data.get("results", [])

    except requests.RequestException as error:
        print(f"TMDB search error: {error}")
        return []


def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"

    params = {
        "api_key": API_KEY
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        print(f"TMDB movie details error: {error}")
        return None