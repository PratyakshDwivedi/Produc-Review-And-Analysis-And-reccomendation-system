"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend import config
from backend.database import connection
from backend.database.store import get_store
from backend.routes import (
    account_routes, analysis_routes, auth_routes, catalog_routes,
    chatbot_routes, recommend_routes,
)

app = FastAPI(title="Product Review Analysis & Recommendation System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for mod in (catalog_routes, analysis_routes, recommend_routes, auth_routes,
            account_routes, chatbot_routes):
    app.include_router(mod.router)


@app.get("/health")
def health():
    """Service health check. Reports the active storage backend."""
    return {
        "status": "ok",
        "mongodb": connection.ping(),
        "storage_backend": get_store().backend,
    }


# Serve the built React frontend as a single app (one port) when it exists.
# Static assets are served directly; any other non-API path returns index.html
# so client-side routing (deep links / refresh) works.
if config.FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=config.FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}")
    def spa(full_path: str):
        if full_path.startswith("api/") or full_path == "health":
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Not found")
        candidate = (config.FRONTEND_DIST / full_path)
        if full_path and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(config.FRONTEND_DIST / "index.html")
