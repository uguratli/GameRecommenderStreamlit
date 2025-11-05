import torch
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
data = torch.load('games_with_embeddings.pt', weights_only=False)
embeddings = np.vstack(data['embedding'].to_numpy())

def genre_similarity(genres_a, genres_b):
    set_a = set(map(str.strip, genres_a.lower().split(',')))
    set_b = set(map(str.strip, genres_b.lower().split(',')))
    return len(set_a & set_b) / len(set_a | set_b) if set_a | set_b else 0

def recommend_games(query, top_n=5, alpha=0.6, beta=0.1, gamma=0.1):

    query_embedding = model.encode(query, convert_to_tensor=True)
    query_embedding = query_embedding.cpu().numpy()

    text_sim = cosine_similarity(
        [query_embedding],
        embeddings)[0]

    results = []
    for i, row in data.iterrows():
        g_sim = genre_similarity(query, row['genres']) if "," in query else 0
        final_score = alpha * text_sim[i] + beta * g_sim + gamma * row['normalized_score']
        results.append((row['game_name'], row['genres'], row['avg_score'], final_score, row['game_summary'], row['game_page']))

    top_results = sorted(results, key=lambda x: x[3], reverse=True)[:top_n]
    return pd.DataFrame(top_results, columns=['Game', 'Genres', 'Score', 'Hybrid_Score', 'Summary', 'Page'])