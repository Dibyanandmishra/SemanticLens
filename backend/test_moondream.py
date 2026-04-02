from moondream import generate_caption, extract_tags

image_path = "dataset/coco_subset/000000002148.jpg"

caption = generate_caption(image_path)
tags = extract_tags(caption)

print("Caption:", caption)
print("Tags:", tags)