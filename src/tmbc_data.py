import sqlite3
import requests
import urllib.parse
import os

API_KEY = "534c070c9fbe944cad05621b481f65f8"

def connect_to_database():
    """
    Connect to the SQLite database.
    """
    db_path = os.path.join(os.path.dirname(__file__), "../database/Movies.db")
    conn = sqlite3.connect(db_path)
    return conn


def get_genres_data(cursor):
    """
    Fetch genres from the TMDb API and populate the genres table.
    """
    genres_url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {"api_key": API_KEY}
    response = requests.get(f"{genres_url}?{urllib.parse.urlencode(params)}")

    if response.status_code == 200:
        genres = response.json().get("genres", [])
        for genre in genres:
            cursor.execute("""
                INSERT OR IGNORE INTO genres (id, name)
                VALUES (?, ?)
            """, (genre["id"], genre["name"]))
        print("Genres table populated successfully.")
    else:
        print(f"Error fetching genres: {response.status_code}")


def fetch_movies(cursor, page):
    """
    Fetch popular movies from the TMDb API and populate the movies table.
    """
    movies_url = "https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": API_KEY, "page": page}
    response = requests.get(f"{movies_url}?{urllib.parse.urlencode(params)}")

    if response.status_code == 200:
        movies = response.json().get("results", [])
        for movie in movies:
            movie_id = movie.get("id")
            title = movie.get("title", "Unknown Title")
            genre_ids = movie.get("genre_ids", [])
            genre_id = genre_ids[0] if genre_ids else None
            popularity = movie.get("popularity", 0.0)
            rating = movie.get("vote_average", None)
            release_date = movie.get("release_date", None)
            revenue = fetch_movie_details(movie_id).get("revenue", None)

            cursor.execute("""
                INSERT OR IGNORE INTO movies (id, title, genre_id, popularity, rating, release_date, revenue)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (movie_id, title, genre_id, popularity, rating, release_date, revenue))
        print(f"Movies added from page {page}.")
    else:
        print(f"Error fetching movies from page {page}: {response.status_code}")



def fetch_movie_details(movie_id):
    """
    Fetch detailed data for a specific movie from TMDb.
    """
    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": API_KEY}
    response = requests.get(f"{details_url}?{urllib.parse.urlencode(params)}")

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching details for movie ID {movie_id}: {response.status_code}")
        return {}


def main():
    """
    Main function to populate the database.
    """
    conn = connect_to_database()
    cursor = conn.cursor()

    # Populate genres table
    get_genres_data(cursor)

    # Populate movies table (fetching data from the first 5 pages of popular movies)
    for page in range(1, 6):
        fetch_movies(cursor, page)

    conn.commit()
    conn.close()
    print("Database successfully populated.")


if __name__ == "__main__":
    main()
