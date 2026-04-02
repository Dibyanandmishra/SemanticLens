import os
import pickle
from feature_extractor import extract_features
from moondream import generate_caption, extract_tags   # ✅ ADD THIS

DATASET_PATH = "dataset/coco_subset"
OUTPUT_FILE = "features.pkl"

features_db = {}

for img_name in os.listdir(DATASET_PATH):
    img_path = os.path.join(DATASET_PATH, img_name)

    try:
        # Step 1: Extract features
        features = extract_features(img_path)

        # Step 2: Generate caption
        caption = generate_caption(img_path)

        # Step 3: Extract tags
        tags = extract_tags(caption)

        # Step 4: Store everything
        features_db[img_name] = {
            "features": features,
            "caption": caption,
            "tags": tags
        }

        print(f"Processed: {img_name}")

    except Exception as e:
        print(f"Skipped: {img_name} | Error: {e}")

# Save database
with open(OUTPUT_FILE, "wb") as f:
    pickle.dump(features_db, f)

print("Indexing complete!")