import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
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

    # Plot the data
    plt.bar(df['genre'], df['total_revenue'] / 1e6, color='skyblue')  # Revenue in millions
    plt.xlabel('Genres')
    plt.ylabel('Total Revenue (in Millions)')
    plt.title('Total Revenue by Genre')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def movie_count_by_language():
    """
    Create a pie chart to display the distribution of movies by language with a key for language codes.
    """
    # Map of language codes to full names
    language_map = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'zh': 'Chinese',
        'ja': 'Japanese',
        'ko': 'Korean',
        'it': 'Italian',
        'hi': 'Hindi',
        'pt': 'Portuguese',
    }

    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT cm.language, COUNT(*) AS movie_count
        FROM movies cm
        GROUP BY cm.language
        ORDER BY movie_count DESC
        LIMIT 10  -- Limit to the top 10 languages for readability
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Replace language codes with full names in the legend
    df['full_language'] = df['language'].map(language_map).fillna('Unknown')

    # Create the pie chart
    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = ax.pie(
        df['movie_count'],
        labels=df['language'],
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.Paired.colors,
        textprops={'fontsize': 8}
    )

    # Add a legend showing both the language code and full name
    legend_labels = [f"{code} = {name}" for code, name in zip(df['language'], df['full_language'])]
    ax.legend(
        wedges,
        legend_labels,
        title="Language Key",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize="small"
    )

    # Title and formatting
    plt.title('Movie Count by Language (Top 10)', fontsize=14)
    plt.axis('equal')  # Ensures the pie chart is circular
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
