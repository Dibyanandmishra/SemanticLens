from search_engine import search

# 1. Image only
print("\n--- Image Search ---")
print(search(image_path="dataset/coco_subset/000000002148.jpg"))

# 2. Text only
print("\n--- Text Search ---")
print(search(text_query="red hydrant"))

# 3. Hybrid
print("\n--- Hybrid Search ---")
print(search(
    image_path="dataset/coco_subset/000000002148.jpg",
    text_query="red"
))