from search_engine import search

results = search("dataset/coco_subset/000000002148.jpg")

for r in results:
    print(r)