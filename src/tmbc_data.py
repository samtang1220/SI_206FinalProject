import sqlite3
import requests
import json
from config import DB_PATH

API_KEY = "534c070c9fbe944cad05621b481f65f8"

def fetch_genres(cursor):
    """
    Fetch genres from the TMDb API and populate the genres table.
    """
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US"
    response = requests.get(url)

    if response.status_code == 200:
        genres = response.json().get("genres", [])
        for genre in genres:
            cursor.execute("""
                INSERT OR IGNORE INTO genres (id, name)
                VALUES (?, ?)
            """, (genre["id"], genre["name"]))
        print("Genres table populated successfully.")
    else:
        print(f"Failed to fetch genres: {response.status_code}")

def fetch_movies(cursor, page):
    """
    Fetch popular movies from the TMDb API and populate the movies table.
    """
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page={page}"
    response = requests.get(url)

    if response.status_code == 200:
        movies = response.json().get("results", [])
        for movie in movies:
            # Second API call to get revenue
            movie_details_url = f"https://api.themoviedb.org/3/movie/{movie['id']}?api_key={API_KEY}&language=en-US"
            movie_details_response = requests.get(movie_details_url)

            if movie_details_response.status_code == 200:
                movie_details = movie_details_response.json()
                revenue = movie_details.get("revenue", 0)
            else:
                revenue = 0  # Default to 0 if the second API call fails

            # Insert movie data into the database
            cursor.execute("""
                INSERT OR IGNORE INTO movies (id, title, genre_id, popularity, rating, release_date, revenue, language)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                movie["id"],
                movie["title"],
                movie["genre_ids"][0] if movie["genre_ids"] else None,
                movie["popularity"],
                movie["vote_average"],
                movie.get("release_date", None),
                revenue,  # Updated with the revenue value from the second API call
                movie.get("original_language", None)
            ))
        print(f"Movies added from page {page}.")
    else:
        print(f"Failed to fetch movies: {response.status_code}")



def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch genres
    fetch_genres(cursor)

    # Fetch movies (fetch from first 20 pages as an example)
    for page in range(1, 21):
        fetch_movies(cursor, page)

    conn.commit()
    conn.close()
    print("Database successfully populated.")

if __name__ == "__main__":
    main()
