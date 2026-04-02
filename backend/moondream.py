from transformers import AutoModelForCausalLM
from PIL import Image
import torch

MODEL_ID = "vikhyatk/moondream2"
REVISION = "2025-06-21"  # Always pin to a specific revision

# Determine device
device = "cuda" if torch.cuda.is_available() else "cpu"

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    revision=REVISION,
    trust_remote_code=True,
    device_map={"": device},
    torch_dtype=torch.float32 if device == "cpu" else torch.float16,
)

def generate_caption(image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")
    result = model.caption(image, length="short")
    return result["caption"]

def extract_tags(caption: str):
    stopwords = {"a", "an", "the", "on", "in", "with", "and", "of", "to", "for", "is", "are"}
    words = [w.strip(".,!?;:").lower() for w in caption.split()]
    return [w for w in words if w and w not in stopwords]