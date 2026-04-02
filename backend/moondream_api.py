import os
import base64
import logging
import time
import requests
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger("semanticlens.moondream")

API_URL = "https://api.moondream.ai/v1/caption"
API_KEY = os.getenv("MOONDREAM_API_KEY")
TIMEOUT_SECONDS = int(os.getenv("MOONDREAM_TIMEOUT", "30"))
MAX_RETRIES = int(os.getenv("MOONDREAM_MAX_RETRIES", "2"))
RETRY_BACKOFF = 1.5

STOPWORDS = frozenset({
    "a", "an", "the", "on", "in", "with", "and",
    "of", "to", "for", "is", "are", "by", "this",
    "that", "it", "at", "from", "as", "was", "were",
    "has", "have", "been", "be", "its", "or", "but",
    "not", "no", "some", "there", "their", "they",
})


def _encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        raw = f.read()
    b64 = base64.b64encode(raw).decode("utf-8")
    ext = os.path.splitext(image_path)[1].lstrip(".").lower()
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(ext, "jpeg")
    return f"data:image/{mime};base64,{b64}"


def generate_caption(image_path: str) -> str:
    if not API_KEY:
        log.warning("MOONDREAM_API_KEY not set — skipping caption generation")
        return ""

    if not os.path.isfile(image_path):
        log.error("Image file not found: %s", image_path)
        return ""

    data_url = _encode_image(image_path)

    payload = {"image_url": data_url, "length": "short"}
    headers = {
        "Content-Type": "application/json",
        "X-Moondream-Auth": API_KEY,
    }

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(
                API_URL, json=payload, headers=headers, timeout=TIMEOUT_SECONDS
            )
            resp.raise_for_status()
            caption = resp.json().get("caption", "")
            log.debug("Caption generated for %s: %s", os.path.basename(image_path), caption[:80])
            return caption

        except requests.exceptions.Timeout:
            last_error = f"Timeout (attempt {attempt}/{MAX_RETRIES})"
            log.warning("%s for %s", last_error, image_path)

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else "unknown"
            last_error = f"HTTP {status} (attempt {attempt}/{MAX_RETRIES})"
            log.warning("%s for %s: %s", last_error, image_path, e)

            if e.response is not None and e.response.status_code in (401, 403):
                log.error("Authentication failed — check your MOONDREAM_API_KEY")
                return ""

        except requests.exceptions.ConnectionError:
            last_error = f"Connection error (attempt {attempt}/{MAX_RETRIES})"
            log.warning("%s for %s", last_error, image_path)

        except Exception as e:
            last_error = str(e)
            log.error("Unexpected error for %s: %s", image_path, e)
            return ""

        if attempt < MAX_RETRIES:
            wait = RETRY_BACKOFF * attempt
            log.info("Retrying in %.1fs...", wait)
            time.sleep(wait)

    log.error("All %d attempts failed for %s — last error: %s", MAX_RETRIES, image_path, last_error)
    return ""


def extract_tags(caption: str) -> list[str]:
    if not caption:
        return []
    cleaned = caption.lower().replace(".", "").replace(",", "").replace("!", "").replace("?", "")
    words = cleaned.split()
    seen = set()
    tags = []
    for w in words:
        if w not in STOPWORDS and w not in seen:
            seen.add(w)
            tags.append(w)
    return tags
