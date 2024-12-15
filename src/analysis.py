import sqlite3
import pandas as pd
from config import DB_PATH

# Analysis 1: Total Votes by Genre
def get_votes_by_genre():
    """
    Retrieves total votes for each genre by aggregating data from the database.
    Returns a Pandas DataFrame with genre_name and total_votes.
    """
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT g.name AS genre_name, SUM(m.vote_count) AS total_votes
        FROM movie_data m
        JOIN genres g ON m.genre_id = g.id
        GROUP BY g.name
        ORDER BY total_votes DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Analysis 2: Average Runtime by Genre
def get_runtime_by_genre():
    """
    Retrieves average runtime for each genre by aggregating data from the database.
    Returns a Pandas DataFrame with genre_name and avg_runtime.
    """
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT g.name AS genre_name, AVG(m.runtime) AS avg_runtime
        FROM movie_data m
        JOIN genres g ON m.genre_id = g.id
        WHERE m.runtime IS NOT NULL
        GROUP BY g.name
        ORDER BY avg_runtime DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Helper Function: Write Output to JSON
def write_output(dataframe, filename):
    """
    Writes the given Pandas DataFrame to a JSON file in the output folder.
    """
    filepath = f"../output/{filename}"
    dataframe.to_json(filepath, orient="records", indent=4)
    print(f"Saved analysis to {filepath}")