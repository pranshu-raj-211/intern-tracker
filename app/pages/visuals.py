from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

df = pd.read_csv('data/processed/2024_03_11.csv')

grouped = df.groupby('query')

for query, group in grouped:
    title_counts = Counter(group['title'])

    wordcloud = WordCloud(background_color="black", colormap='viridis', width=800, height=400).generate_from_frequencies(title_counts)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(f'Word Cloud for Query: {query}', fontsize=20, fontweight='bold')

    wordcloud.to_file(f"static/wordcloud/{query}.png")

    plt.show()