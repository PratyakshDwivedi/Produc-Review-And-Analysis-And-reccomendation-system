"""Single entry point: build the frontend (if needed) and run the full app.

Serves the React UI and the API together from one server:
    http://127.0.0.1:8000

Usage:
    python run.py            # build frontend if missing, then serve
    python run.py --build    # force a fresh frontend build first
"""
import subprocess
import sys
from pathlib import Path

import uvicorn

ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "frontend"
DIST = FRONTEND / "dist"


def build_frontend() -> None:
    npm = "npm.cmd" if sys.platform == "win32" else "npm"
    if not (FRONTEND / "node_modules").exists():
        subprocess.run([npm, "install"], cwd=FRONTEND, check=True)
    subprocess.run([npm, "run", "build"], cwd=FRONTEND, check=True)


if __name__ == "__main__":
    if "--build" in sys.argv or not DIST.exists():
        build_frontend()
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000)
