import os
import requests
from tqdm import tqdm
from pycocotools.coco import COCO

# Path to annotation file
annFile = 'annotations/instances_train2017.json'

# Load COCO
coco = COCO(annFile)

# Get 300 random images
import random
img_ids = coco.getImgIds()
selected_ids = random.sample(img_ids, 300)

# Create folder
os.makedirs('coco_subset', exist_ok=True)

# Download images
for img_id in tqdm(selected_ids):
    img = coco.loadImgs(img_id)[0]
    url = img['coco_url']
    
    try:
        img_data = requests.get(url, timeout=10).content
        with open(f'coco_subset/{img["file_name"]}', 'wb') as f:
            f.write(img_data)
    except:
        continue

print("✅ Done! 300 images downloaded.")