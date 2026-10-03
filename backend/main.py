"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
