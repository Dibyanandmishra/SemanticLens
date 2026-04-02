import os
import sys
import shutil
import logging
import tempfile
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("semanticlens.app")

sys.path.insert(0, str(Path(__file__).resolve().parent))

from search_engine import search, features_db, captions_cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    api_key = os.getenv("MOONDREAM_API_KEY")
    if not api_key:
        log.warning("MOONDREAM_API_KEY is not set — caption generation will fail")
    else:
        log.info("Moondream API key loaded")

    log.info(
        "Startup complete — %d indexed images, %d cached captions",
        len(features_db),
        len(captions_cache),
    )
    yield
    log.info("Shutting down")


app = FastAPI(
    title="SemanticLens API",
    description="AI-powered visual search engine with semantic understanding",
    version="2.0.0",
    lifespan=lifespan,
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


def _save_upload(upload: UploadFile) -> str:
    suffix = Path(upload.filename).suffix if upload.filename else ".jpg"
    suffix = suffix or ".jpg"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=str(UPLOAD_DIR))
    shutil.copyfileobj(upload.file, tmp)
    tmp.close()
    return tmp.name


def _cleanup(path: str):
    try:
        os.unlink(path)
    except OSError:
        pass


def _validate_image(file: UploadFile):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Upload must be an image file (JPEG, PNG, or WebP)")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "indexed_images": len(features_db),
        "cached_captions": len(captions_cache),
    }


@app.post("/search-by-image")
@limiter.limit("5/minute")
async def search_by_image(
    request: Request,
    file: UploadFile = File(...),
    top_k: int = Form(default=5),
):
    _validate_image(file)

    if top_k < 1 or top_k > 50:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 50")

    saved_path = _save_upload(file)
    try:
        results = search(image_path=saved_path, top_k=top_k)
        return {"results": results, "count": len(results), "mode": "image"}
    except Exception as e:
        log.exception("search-by-image failed")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        _cleanup(saved_path)


@app.post("/search-by-text")
@limiter.limit("10/minute")
async def search_by_text(
    request: Request,
    query: str = Form(...),
    top_k: int = Form(default=5),
):
    query = query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query text cannot be empty")

    if top_k < 1 or top_k > 50:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 50")

    try:
        results = search(text_query=query, top_k=top_k)
        return {"results": results, "count": len(results), "mode": "text"}
    except Exception as e:
        log.exception("search-by-text failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search-hybrid")
@limiter.limit("5/minute")
async def search_hybrid(
    request: Request,
    file: UploadFile = File(...),
    query: str = Form(...),
    top_k: int = Form(default=5),
):
    _validate_image(file)
    query = query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query text cannot be empty")

    if top_k < 1 or top_k > 50:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 50")

    saved_path = _save_upload(file)
    try:
        results = search(image_path=saved_path, text_query=query, top_k=top_k)
        return {"results": results, "count": len(results), "mode": "hybrid"}
    except Exception as e:
        log.exception("search-hybrid failed")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        _cleanup(saved_path)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    log.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
