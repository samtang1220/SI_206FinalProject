import sqlite3
import os

def connect_to_database():
    """
    Connect to the SQLite database. If the database doesn't exist, create it.
    """
    # Define the database path relative to this script
    db_path = os.path.join(os.path.dirname(__file__), "../database/Movies.db")

    # Ensure the database folder exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Connect to the database
    conn = sqlite3.connect(db_path)
    return conn


def create_tables(conn):
    """
    Create the necessary tables for the project in the database.
    """
    cur = conn.cursor()

    # Drop tables if they already exist (optional for reset)
    cur.execute("DROP TABLE IF EXISTS movies;")
    cur.execute("DROP TABLE IF EXISTS genres;")

    # Create genres table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')

    # Create movies table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title TEXT,
            genre_id INTEGER,
            popularity REAL,
            rating REAL,
            release_date TEXT,
            revenue INTEGER,
            language TEXT,
            FOREIGN KEY (genre_id) REFERENCES genres (id)
        )
    ''')

    conn.commit()


def main():
    """
    Main function to initialize the database and create tables.
    """
    conn = connect_to_database()
    create_tables(conn)
    print("Database initialized and tables created successfully.")
    conn.close()


if __name__ == "__main__":
    main()
