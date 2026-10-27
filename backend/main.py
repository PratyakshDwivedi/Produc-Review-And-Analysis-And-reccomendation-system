"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
# API routes above take precedence; unknown non-API paths fall back to index.html.
if config.FRONTEND_DIST.exists():
    app.mount(
        "/", StaticFiles(directory=config.FRONTEND_DIST, html=True), name="frontend"
    )
