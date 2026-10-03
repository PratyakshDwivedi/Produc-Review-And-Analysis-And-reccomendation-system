"""Vercel serverless entry point.

Vercel serves the exported ASGI `app` for requests routed here by vercel.json
(/api/* and /health). The React frontend is served separately as static files
from frontend/dist. Locally, prefer `python run.py` (single server).
"""
import os
import sys

# Ensure the repo root is importable so `backend` resolves inside the bundle.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.main import app  # noqa: E402,F401
