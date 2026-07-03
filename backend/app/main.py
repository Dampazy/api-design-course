from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app import models  # noqa: F401  (ensures models are registered on Base)
from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models.theory import TheoryBlock
from app.routers import progress, stats, tasks, theory

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Design Course Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(theory.router)
app.include_router(tasks.router)
app.include_router(progress.router)
app.include_router(stats.router)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.on_event("startup")
def seed_if_empty() -> None:
    """On a fresh deploy (e.g. Render's ephemeral filesystem after a
    restart) the SQLite file has no content yet — seed it automatically so
    the site works without a manual release step."""
    db = SessionLocal()
    try:
        if db.query(TheoryBlock).count() == 0:
            from app.seed.seed import run as seed_run

            seed_run()
    finally:
        db.close()


# Serve the built React app (frontend/dist) from the same FastAPI process in
# production, so there is a single deployable service and a single URL —
# no separate static host, no CORS between frontend/backend origins.
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"

if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str) -> FileResponse:
        candidate = FRONTEND_DIST / full_path
        if full_path and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(FRONTEND_DIST / "index.html")
