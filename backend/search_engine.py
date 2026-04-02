import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from feature_extractor import extract_features

# Load database
with open("features.pkl", "rb") as f:
    features_db = pickle.load(f)

def search(image_path, top_k=5):
    query_vec = extract_features(image_path)

    similarities = []

    for img_name, vec in features_db.items():
        sim = cosine_similarity([query_vec], [vec])[0][0]
        similarities.append((img_name, sim))

    # Sort by similarity
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:top_k]