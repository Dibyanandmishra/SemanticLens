from feature_extractor import extract_features

vec = extract_features("dataset/coco_subset/000000002148.jpg")
print(len(vec))