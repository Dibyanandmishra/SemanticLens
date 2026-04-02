import logging
import pickle
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

from feature_extractor import extract_features
from moondream_api import generate_caption, extract_tags

log = logging.getLogger("semanticlens.search")

BASE_DIR = Path(__file__).resolve().parent.parent
FEATURES_FILE = BASE_DIR / "features.pkl"
CACHE_FILE = BASE_DIR / "cache" / "captions_cache.pkl"
DATASET_DIR = BASE_DIR / "dataset" / "coco_subset"


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------

def _load_features_db() -> dict:
    if not FEATURES_FILE.exists():
        log.warning("Features file not found at %s — starting with empty DB", FEATURES_FILE)
        return {}
    with open(FEATURES_FILE, "rb") as f:
        db = pickle.load(f)
    log.info("Loaded %d image feature vectors", len(db))
    return db


def _load_cache() -> dict:
    if not CACHE_FILE.exists():
        return {}
    with open(CACHE_FILE, "rb") as f:
        cache = pickle.load(f)
    log.info("Loaded %d cached captions", len(cache))
    return cache


def _save_cache(cache: dict):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cache, f)


# ---------------------------------------------------------------------------
# Module-level state (loaded once at import / startup)
# ---------------------------------------------------------------------------

features_db: dict = _load_features_db()
captions_cache: dict = _load_cache()


# ---------------------------------------------------------------------------
# Step 3 + 4: Caption generation with caching
# ---------------------------------------------------------------------------

def _get_caption_and_tags(img_name: str) -> tuple[str, list[str]]:
    global captions_cache

    if img_name in captions_cache:
        entry = captions_cache[img_name]
        return entry["caption"], entry["tags"]

    img_path = str(DATASET_DIR / img_name)
    caption = generate_caption(img_path)
    tags = extract_tags(caption)

    captions_cache[img_name] = {"caption": caption, "tags": tags}
    _save_cache(captions_cache)
    log.debug("Cached caption for %s", img_name)

    return caption, tags


# ---------------------------------------------------------------------------
# Step 1: Visual feature similarity
# ---------------------------------------------------------------------------

def _compute_visual_scores(query_vec: np.ndarray) -> list[tuple[str, float]]:
    names = list(features_db.keys())
    if not names:
        return []
    vectors = np.array([features_db[n]["features"] for n in names])
    scores = cosine_similarity([query_vec], vectors)[0]
    return list(zip(names, scores.tolist()))


# ---------------------------------------------------------------------------
# Main search pipeline
# ---------------------------------------------------------------------------

def search(
    image_path: str | None = None,
    text_query: str | None = None,
    top_k: int = 5,
) -> list[dict]:
    """
    5-step search pipeline:
      1. Feature similarity  — compute cosine scores against the DB
      2. Top-K selection     — take the best visual candidates
      3. Caption generation  — call Moondream API for each candidate
      4. Caching             — persist generated captions so we never re-call
      5. Text filtering      — optionally filter by keyword match on tags
    """
    if not image_path and not text_query:
        return []

    if not features_db:
        log.error("Feature database is empty — run index_dataset.py first")
        return []

    # Step 1 + 2: visual ranking
    if image_path:
        query_vec = extract_features(image_path)
        scored = _compute_visual_scores(query_vec)
        scored.sort(key=lambda x: x[1], reverse=True)
        candidate_count = top_k * 3 if text_query else top_k
        candidates = scored[:candidate_count]
    else:
        candidates = [(name, 0.0) for name in features_db.keys()]

    # Step 3 + 4 + 5: caption, cache, filter
    results = []
    for img_name, score in candidates:
        caption, tags = _get_caption_and_tags(img_name)

        if text_query:
            query_words = set(text_query.lower().split())
            if not query_words.intersection(tags):
                continue

        results.append({
            "image": img_name,
            "score": round(float(score), 4),
            "caption": caption,
            "tags": tags,
        })

        if len(results) >= top_k:
            break

    log.info(
        "Search complete — mode=%s, candidates=%d, results=%d",
        "hybrid" if image_path and text_query else ("image" if image_path else "text"),
        len(candidates),
        len(results),
    )
    return results