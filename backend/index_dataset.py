import os
import pickle
from feature_extractor import extract_features

DATASET_PATH = "dataset/coco_subset"
OUTPUT_FILE = "features.pkl"

features_db = {}

for img_name in sorted(os.listdir(DATASET_PATH))[:20]:
    img_path = os.path.join(DATASET_PATH, img_name)

    try:
        # Only extract features (FAST)
        features = extract_features(img_path)

        features_db[img_name] = {
            "features": features
        }

        print(f"Processed: {img_name}")

    except Exception as e:
        print(f"Skipped: {img_name} | Error: {e}")

# Save database
with open(OUTPUT_FILE, "wb") as f:
    pickle.dump(features_db, f)

print("Indexing complete!")