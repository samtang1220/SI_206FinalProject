import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../database/data.db")

def connect_to_database():
    """
    Connect to the SQLite database. If the database doesn't exist, create it.
    """
    # Ensure the database folder exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_types_table(cur):
    """
    Create the Pokémon types table.
    """
    cur.execute("""
    CREATE TABLE IF NOT EXISTS types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_name TEXT UNIQUE
    );
    """)

def create_pokemon_table(cur):
    """
    Create the Pokémon table.
    """
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pokemons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        type_id INTEGER,
        attack REAL,
        defense REAL,
        speed REAL,
        FOREIGN KEY (type_id) REFERENCES types (id)
    );
    """)

def create_movies_and_genres_tables(cur):
    """
    Create the Movies and Genres tables.
    """
    # Create genres table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS genres (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    """)

    # Create movies table
    cur.execute("""
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
    );
    """)

def initialize_database():
    """
    Initialize the database with all required tables.
    """
    conn = connect_to_database()
    cur = conn.cursor()

    # Create Pokémon tables (types and pokemons)
    create_types_table(cur)
    create_pokemon_table(cur)

    # Create Movies and Genres tables
    create_movies_and_genres_tables(cur)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()
