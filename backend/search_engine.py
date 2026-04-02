import pickle
from pathlib import Path
import numpy as np

try:
    from .feature_extractor import extract_features
    from .moondream_api import generate_caption
except ImportError:
    from feature_extractor import extract_features
    from moondream_api import generate_caption

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE = Path(__file__).resolve().parent / "index.pkl"


def _load_index() -> list[dict]:
    if not INDEX_FILE.exists():
        raise FileNotFoundError(f"Index file missing at {INDEX_FILE}. Run backend/indexer.py first.")
    with open(INDEX_FILE, "rb") as handle:
        index_data = pickle.load(handle)
    print(f"[search_engine] loaded {len(index_data)} indexed images")
    return index_data


def search_similar_images(query_image_path: str, top_k: int = 5) -> list[dict]:
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    index_data = _load_index()
    if not index_data:
        raise RuntimeError("Index is empty. Rebuild index with backend/indexer.py.")

    query_features = extract_features(query_image_path)
    ranked = []

    for item in index_data:
        db_features = np.asarray(item["features"], dtype=np.float32)
        distance = float(np.linalg.norm(query_features - db_features))
        ranked.append({"image": item["image"], "distance": round(distance, 6)})

    ranked.sort(key=lambda item: item["distance"])
    top_results = ranked[:top_k]

    print("[search_engine] top distances:", [row["distance"] for row in top_results])
    return top_results


def run_search_pipeline(query_image_path: str, text_query: str | None = None, top_k: int = 5) -> dict:
    caption = generate_caption(query_image_path)
    print("Caption:", caption)

    results = search_similar_images(query_image_path, top_k=top_k)
    print("Results:", results)

    if text_query:
        lowered = text_query.lower().strip()
        if lowered and caption and lowered not in caption.lower():
            print("[search_engine] text query does not match caption; returning visual results only")

    return {"caption": caption, "images": ["/" + row["image"].lstrip("/") for row in results], "results": results}