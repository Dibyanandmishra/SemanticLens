import pickle
from pathlib import Path

try:
    from .feature_extractor import extract_features
except ImportError:
    from feature_extractor import extract_features


BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset" / "coco_subset"
INDEX_FILE = Path(__file__).resolve().parent / "index.pkl"
VALID_EXT = {".jpg", ".jpeg", ".png", ".webp"}


def build_index() -> int:
    if not DATASET_DIR.exists():
        raise FileNotFoundError(f"Dataset directory not found: {DATASET_DIR}")

    entries = []
    image_paths = [p for p in sorted(DATASET_DIR.iterdir()) if p.suffix.lower() in VALID_EXT]
    print(f"[indexer] found {len(image_paths)} candidate images")

    for image_path in image_paths:
        try:
            vector = extract_features(str(image_path))
            entries.append({"image": str(image_path.relative_to(BASE_DIR)).replace("\\", "/"), "features": vector})
            print(f"[indexer] indexed: {image_path.name}")
        except Exception as error:
            print(f"[indexer] skipped corrupted image: {image_path.name} ({error})")

    with open(INDEX_FILE, "wb") as handle:
        pickle.dump(entries, handle)

    print(f"[indexer] index saved: {INDEX_FILE}")
    print(f"[indexer] total indexed images: {len(entries)}")

    if len(entries) < 50:
        raise RuntimeError(f"Expected at least 50 images indexed, got {len(entries)}")

    return len(entries)


if __name__ == "__main__":
    build_index()
