import sqlite3
import requests
import json
from config import DB_PATH, API_KEY

def fetch_data(url):
    headers = {"User-Agent": "SI206-Movie-Stats-Project"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_movie_data(target=100, max_per_run=20):
    db_connection = sqlite3.connect(DB_PATH)
    db_cursor = db_connection.cursor()

    # Check the current count of movies in the database
    db_cursor.execute("SELECT COUNT(DISTINCT id) FROM movies")
    current_count = db_cursor.fetchone()[0]

    if current_count >= target:
        print(f"Final movie count: {current_count} movies.")
        db_connection.close()
        return

    remaining = target - current_count
    limit = min(remaining, max_per_run)

    added_movies = 0
    page = 1
    while added_movies < limit:
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page={page}"
        try:
            data = fetch_data(url)
            movies = data.get("results", [])

            if not movies:
                break

            movie_batch = []
            genre_batch = []
            for movie in movies:
                # Avoid adding duplicates by checking database first
                db_cursor.execute("SELECT COUNT(*) FROM movies WHERE id = ?", (movie["id"],))
                if db_cursor.fetchone()[0] > 0:
                    continue

                movie_details_url = f"https://api.themoviedb.org/3/movie/{movie['id']}?api_key={API_KEY}&language=en-US"
                movie_details = fetch_data(movie_details_url)

                genre_id = movie_details["genres"][0]["id"] if movie_details["genres"] else None
                genre_name = movie_details["genres"][0]["name"] if movie_details["genres"] else None
                revenue = movie_details.get("revenue", 0)

                if genre_id and genre_name:
                    genre_batch.append((genre_id, genre_name))

                movie_batch.append((
                    movie["id"],
                    movie["title"],
                    genre_id,
                    movie["popularity"],
                    movie["vote_average"],
                    movie.get("release_date", None),
                    revenue,
                    movie.get("original_language", None),
                ))

                added_movies += 1
                if added_movies >= limit:
                    break

            # Insert data into the database
            db_cursor.executemany("INSERT OR IGNORE INTO genres (id, name) VALUES (?, ?)", genre_batch)
            db_cursor.executemany(
                """
                INSERT OR IGNORE INTO movies (id, title, genre_id, popularity, rating, release_date, revenue, language)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                movie_batch
            )
            db_connection.commit()

            if added_movies > 0:
                print(f"Added {len(movie_batch)} new movies from page {page}. Current total: {current_count + added_movies} movies.")
            page += 1

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    print(f"Final movie count: {current_count + added_movies} movies.")
    db_connection.close()

if __name__ == "__main__":
    fetch_movie_data(target=100, max_per_run=20)
