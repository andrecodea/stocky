from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from dotenv import load_dotenv
import logging
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

app = FastAPI(title="Stocky - Inventory Management")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTML docs
DOCS_DIR = (Path(__file__).resolve().parent / "docs" / "build" / "html")
if DOCS_DIR.exists():
    app.mount("/html/docs", StaticFiles(directory=str(DOCS_DIR), html=True), name="html_docs")
else:
    print(f"[WARN] Sphinx HTML not found at: {DOCS_DIR}. Run: cd docs && mkdir html")


# Publicos
@app.get("/ping", tags=["Test"])
def ping(): return {"pong": True}

@app.get("/health", include_in_schema=False)
def health(): return {"status": "ok"}

if __name__ == '__main__':
    logger.info("--- Application starts ---")
    uvicorn.run(
        "app:app",
        host=config.api['SERVER_HOST'],
        port=config.api['SERVER_PORT'],
        reload=True
    )
    logger.info("--- Application ends ---")