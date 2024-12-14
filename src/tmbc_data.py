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


def fetch_movies_data(cursor, page):
    """
    Fetch popular movies and populate movie_data table.
    """
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": "534c070c9fbe944cad05621b481f65f8", "page": page}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        movies = response.json().get("results", [])
        for movie in movies:
            movie_id = movie.get("id")
            title = movie.get("title", "Unknown Title")
            genre_ids = movie.get("genre_ids", [])
            genre_id = genre_ids[0] if genre_ids else None
            popularity = movie.get("popularity", 0.0)
            avg_rating = movie.get("vote_average", None)
            vote_count = movie.get("vote_count", None)
            release_date = movie.get("release_date", None)
            
            # Fetch detailed data (runtime, revenue)
            detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
            detail_response = requests.get(detail_url, params={"api_key": "534c070c9fbe944cad05621b481f65f8"})
            detail_data = detail_response.json() if detail_response.status_code == 200 else {}
            runtime = detail_data.get("runtime", None)
            revenue = detail_data.get("revenue", None)
            language = movie.get("original_language", "Unknown")

            cursor.execute("""
                INSERT OR IGNORE INTO movie_data 
                (movie_id, title, genre_id, popularity, avg_rating, vote_count, release_date, revenue, runtime, language)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (movie_id, title, genre_id, popularity, avg_rating, vote_count, release_date, revenue, runtime, language))
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
        fetch_movies_data(cursor, page)

    conn.commit()
    conn.close()
    print("Database successfully populated.")


if __name__ == "__main__":
    main()
