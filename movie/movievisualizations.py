import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from config import DB_PATH


def genre_revenue_bar_chart():
    """
    Create a bar chart to show total revenue by genre.
    """
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT g.name AS genre, SUM(m.revenue) AS total_revenue
        FROM movies m
        JOIN genres g ON m.genre_id = g.id
        WHERE m.revenue IS NOT NULL AND m.revenue > 0
        GROUP BY g.name
        ORDER BY total_revenue DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    plt.figure(figsize=(10, 6))
    bars = plt.bar(df['genre'], df['total_revenue'] / 1e6, color='lightpink', edgecolor='blue', linewidth=1.5)  # Revenue in millions

    plt.xlabel('Genres')
    plt.ylabel('Total Revenue (in Millions)')
    plt.title('Total Revenue by Genre')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def movie_count_by_language(n=5):
    """
    Create a pie chart for movie counts by language, showing the top N languages
    and aggregating others into an "Others" category. Adjust percentage labels to be at the circle's edge.
    """
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    
    # Query the database for movie counts by language
    query = """
        SELECT language, COUNT(*) AS movie_count
        FROM movies
        GROUP BY language
        ORDER BY movie_count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Separate top N languages and aggregate the rest
    top_n = df.head(n)
    others = pd.DataFrame([{
        "language": "Others",
        "movie_count": df["movie_count"].iloc[n:].sum()
    }])
    df_combined = pd.concat([top_n, others], ignore_index=True)

    # Create the pie chart
    plt.figure(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(
        df_combined["movie_count"],
        labels=df_combined["language"],
        autopct='%1.1f%%',
        startangle=140,
        colors=cm.Paired.colors,
        textprops={'fontsize': 9}  # Reduce font size
    )

    # Move percentages outward
    for autotext, wedge in zip(autotexts, wedges):
        x, y = autotext.get_position()
        angle = wedge.theta2 - (wedge.theta2 - wedge.theta1) / 2
        x_offset = 1.4 * x
        y_offset = 1.4 * y
        autotext.set_position((x_offset, y_offset))

    plt.title('Movie Count by Language (Top 5 + Others)', fontsize=12)
    
    # Add a legend to explain the language codes
    legend_labels = {
        "en": "English",
        "ja": "Japanese",
        "es": "Spanish",
        "ko": "Korean",
        "fr": "French",
        # "it": "Italian",
        # "zh": "Chinese",
        "Others": "All Other Languages"
    }
    legend_text = "\n".join([f"{k} = {v}" for k, v in legend_labels.items()])
    plt.figtext(0.9, 0.5, legend_text, fontsize=8, ha="left", wrap=True)

    plt.tight_layout()
    plt.show()

    
def main():
    """
    Generate visualizations based on the updated database.
    """
    genre_revenue_bar_chart()  # Bar chart for total revenue by genre
    movie_count_by_language()  # Scatter plot for popularity vs revenue


if __name__ == "__main__":
    main()
