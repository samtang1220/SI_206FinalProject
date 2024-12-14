import sqlite3
from config import DB_PATH

def most_popular_movies():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Query the 10 most popular movies
    cur.execute("""
        SELECT title, popularity
        FROM movies
        ORDER BY popularity DESC
        LIMIT 10
    """)
    results = cur.fetchall()

    conn.close()
    return results

if __name__ == "__main__":
    popular_movies = most_popular_movies()
    for movie in popular_movies:
        print(f"Title: {movie[0]}, Popularity: {movie[1]}")