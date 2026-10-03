"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend import config
from backend.database import connection
from backend.routes import product_routes, review_routes

app = FastAPI(title="Product Review Analysis & Recommendation System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_routes.router)
app.include_router(review_routes.router)


@app.get("/health")
def health():
    """Service health check. Reports whether MongoDB is reachable."""
    return {"status": "ok", "mongodb": connection.ping()}


# Serve the built React frontend as a single app (one port) when it exists.
# Build it with `npm run build` in frontend/. API routes above take precedence.
if config.FRONTEND_DIST.exists():
    app.mount(
        "/", StaticFiles(directory=config.FRONTEND_DIST, html=True), name="frontend"
    )
