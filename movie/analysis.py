import sqlite3
import pandas as pd
import os
from config import DB_PATH

# Ensure the output folder exists
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Analysis 1: Total Popularity by Genre
def get_popularity_by_genre():
    """
    Retrieves total popularity for each genre by aggregating data from the database.
    Returns a Pandas DataFrame with genre_name and total_popularity.
    """
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT g.name AS genre_name, SUM(m.popularity) AS total_popularity
        FROM movies m
        JOIN genres g ON m.genre_id = g.id
        GROUP BY g.name
        ORDER BY total_popularity DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Analysis 2: Average Revenue by Genre
def calculate_avg_revenue_by_genre():
    """
    Calculates the average revenue for each genre.
    Returns a Pandas DataFrame with genre_name and avg_revenue.
    """
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT g.name AS genre_name, AVG(m.revenue) AS avg_revenue
        FROM movies m
        JOIN genres g ON m.genre_id = g.id
        WHERE m.revenue > 0
        GROUP BY g.name
        ORDER BY avg_revenue DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Helper Function: Write Output to a Single Text File
def write_output_to_calc(dataframes, filename):
    """
    Writes multiple DataFrame analyses to a single text file in the output folder.
    """
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w") as file:
        for title, dataframe in dataframes:
            file.write(f"\n{title}\n")
            file.write(dataframe.to_string(index=False))
            file.write("\n\n")
    print(f"Saved combined analysis to {filepath}")

if __name__ == "__main__":
    # Perform analyses
    popularity_by_genre_df = get_popularity_by_genre()
    avg_revenue_by_genre_df = calculate_avg_revenue_by_genre()

    # Write results to a single text file
    write_output_to_calc([
        ("# Analysis 1: Total Popularity by Genre", popularity_by_genre_df),
        ("# Analysis 2: Average Revenue by Genre", avg_revenue_by_genre_df)
    ], "calc.txt")
