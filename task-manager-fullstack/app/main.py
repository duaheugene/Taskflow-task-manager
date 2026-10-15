from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .database import Base, engine
from . import models  # noqa: F401 - registers SQLAlchemy models
from .routes import router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Task Manager API", version="1.0.0", description="A full-stack task manager with per-user task privacy and JWT authentication.")
app.include_router(router)
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
def homepage():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}
