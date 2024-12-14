import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from config import DB_PATH

def genre_popularity_pie_chart(df):
    """
    Create a pie chart to show average popularity by genre.
    """
    plt.pie(
        df['avg_popularity'],
        labels=df['name'],
        autopct=lambda pct: f'{pct:.1f}%',  # Display percentages with 1 decimal place
        startangle=140,
        colors=plt.cm.Paired.colors,
        textprops={'fontsize': 8}  # Reduce font size of labels
    )
    plt.title('Average Popularity Share by Genre (Pie Chart)')
    plt.axis('equal')  # Ensures the pie chart is circular
    plt.tight_layout()
    plt.show()


def genre_revenue_bar_chart(conn):
    """
    Create a vertical bar chart to show average revenue by genre.
    """
    query = """
        SELECT g.name, AVG(m.revenue) as avg_revenue
        FROM movies m
        JOIN genres g ON m.genre_id = g.id
        WHERE m.revenue IS NOT NULL
        GROUP BY g.name
        ORDER BY avg_revenue DESC
    """
    df = pd.read_sql_query(query, conn)

    # Plot the data
    plt.bar(df['name'], df['avg_revenue'], color='lightcoral')
    plt.xlabel('Genres')
    plt.ylabel('Average Revenue (in billions)')
    plt.title('Average Revenue by Genre')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    """
    Fetch data from the database and create visualizations.
    """
    conn = sqlite3.connect(DB_PATH)

    # Popularity Chart (Pie)
    query_popularity = """
        SELECT g.name, AVG(m.popularity) as avg_popularity
        FROM movies m
        JOIN genres g ON m.genre_id = g.id
        GROUP BY g.name
        ORDER BY avg_popularity DESC
    """
    df_popularity = pd.read_sql_query(query_popularity, conn)
    genre_popularity_pie_chart(df_popularity)

    # Revenue Chart (Bar)
    genre_revenue_bar_chart(conn)

    conn.close()


if __name__ == "__main__":
    main()
