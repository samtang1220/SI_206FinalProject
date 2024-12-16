import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def create_visualizations(type_counts):
    # bar chart
    types = [row[0] for row in type_counts]
    counts = [row[1] for row in type_counts]

    colors = cm.viridis(np.linspace(0.2, 0.8, len(types)))

    plt.figure(figsize=(10, 6))
    plt.bar(types, counts, color=colors, edgecolor="black")
    plt.xlabel('Pokémon Type', fontsize=12, fontweight='bold')
    plt.ylabel('Count', fontsize=12, fontweight='bold')
    plt.title('Pokémon Count by Type', fontsize=14, fontweight='bold', color='darkblue')
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # pie chart
    labels = types
    sizes = counts

    pie_colors = cm.plasma(np.linspace(0.2, 0.8, len(sizes)))

    plt.figure(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=pie_colors,
        textprops={'fontsize': 10, 'color': 'black'},
        wedgeprops={'edgecolor': 'black'}
    )

    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")

    plt.title('Pokémon Distribution by Type', fontsize=14, fontweight='bold', color='purple')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # example data for testing
    sample_type_counts = [("Water", 25), ("Fire", 10), ("Grass", 15), ("Electric", 8), ("Normal", 20)]
    create_visualizations(sample_type_counts)
