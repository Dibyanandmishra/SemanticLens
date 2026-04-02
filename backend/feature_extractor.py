from pathlib import Path
import cv2
import numpy as np


def extract_features(image_path: str) -> np.ndarray:
    path = Path(image_path)
    print(f"[feature_extractor] reading image: {path}")

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"OpenCV failed to decode image: {image_path}")

    resized = cv2.resize(image, (224, 224))
    histogram = cv2.calcHist([resized], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    histogram = cv2.normalize(histogram, histogram).flatten().astype(np.float32)
    print(f"[feature_extractor] extracted feature length: {histogram.shape[0]}")
    return histogram