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
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("semanticlens.app")

sys.path.insert(0, str(Path(__file__).resolve().parent))

from search_engine import run_search_pipeline, _load_index


@asynccontextmanager
async def lifespan(app: FastAPI):
    api_key = os.getenv("MOONDREAM_API_KEY")
    if not api_key:
        log.warning("MOONDREAM_API_KEY is not set — caption generation will fail")
    else:
        log.info("Moondream API key loaded")

    indexed_images = len(_load_index())
    log.info("Startup complete — %d indexed images", indexed_images)

    yield
    log.info("Shutting down")


app = FastAPI(
    title="SemanticLens API",
    description="AI-powered visual search engine with semantic understanding",
    version="2.0.0",
    lifespan=lifespan,
)

# ✅ FIXED CORS (IMPORTANT FOR DEPLOYMENT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (safe for demo)
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR.mkdir(exist_ok=True)

# ✅ Serve dataset images
app.mount("/dataset", StaticFiles(directory=str(BASE_DIR / "dataset")), name="dataset")


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
        raise HTTPException(status_code=400, detail="Upload must be an image file")


@app.get("/health")
async def health():
    indexed_images = len(_load_index())
    return {
        "status": "ok",
        "indexed_images": indexed_images,
    }


@app.post("/search")
async def search(
    request: Request,
    file: UploadFile = File(...),
    query: str | None = Form(default=None),
    top_k: int = Form(default=5),
):
    log.info(
        "Request received: /search file=%s query=%s top_k=%s",
        file.filename,
        query or "",
        top_k,
    )

    _validate_image(file)

    if top_k < 1 or top_k > 50:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 50")

    saved_path = _save_upload(file)

    try:
        payload = run_search_pipeline(saved_path, text_query=query, top_k=top_k)
        return payload

    except Exception as e:
        log.exception("/search failed")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        _cleanup(saved_path)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log.exception("Unhandled exception")

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )