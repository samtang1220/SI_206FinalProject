import sqlite3
from config import DB_PATH

def avg_popularity_by_genre():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    query = '''
        SELECT g.name, AVG(m.popularity) AS avg_popularity
        FROM movies m
        JOIN genres g ON m.genre_id = g.id
        GROUP BY g.name;
    '''
    cur.execute(query)
    results = cur.fetchall()
    with open("calc.txt", "a") as file:
        file.write("Average Popularity by Genre:\n")
        for genre, avg_popularity in results:
            file.write(f"{genre}: {avg_popularity:.2f}\n")
    conn.close()

def movie_count_by_language():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    query = '''
        SELECT m.language, COUNT(*) AS movie_count
        FROM movies m
        GROUP BY m.language;
    '''
    cur.execute(query)
    results = cur.fetchall()
    with open("calc.txt", "a") as file:
        file.write("\nMovie Count by Language:\n")
        for language, count in results:
            file.write(f"{language}: {count}\n")
    conn.close()

if __name__ == "__main__":
    avg_popularity_by_genre()
    movie_count_by_language()
