import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from feature_extractor import extract_features

# Load database
with open("features.pkl", "rb") as f:
    features_db = pickle.load(f)

def text_similarity(query, tags):
    query_words = query.lower().split()
    match_count = 0

    for word in query_words:
        if word in tags:
            match_count += 1

    return match_count / len(query_words) if query_words else 0

def search(image_path=None, text_query=None, top_k=5):
    query_vec = None

    if image_path:
        query_vec = extract_features(image_path)

    results = []

    for img_name, data in features_db.items():
        score = 0

        # Image similarity
        if query_vec is not None:
            img_vec = data["features"]
            img_sim = cosine_similarity([query_vec], [img_vec])[0][0]
            score += 0.7 * img_sim

        # Text similarity
        if text_query:
            txt_sim = text_similarity(text_query, data["tags"])
            score += 0.3 * txt_sim

        results.append((img_name, score))

    results.sort(key=lambda x: x[1], reverse=True)

    return results[:top_k]