# Product Review Analysis & Recommendation System

An AI/NLP-powered web app that analyzes product reviews and turns them into
clear, explainable insights: sentiment, aspect-based sentiment, strengths and
weaknesses, summaries, trends, authenticity risk, and natural-language
recommendations — plus accounts, wishlist, price tracking, alerts, and a
retrieval chatbot.

> The bundled dataset is **synthetic demo data** for development only. It does
> not represent real products or real customer reviews. All analysis is computed
> from this text at runtime; nothing is hard-coded.

## Features

**Core intelligence (V1)**
- Product search & overview (computed rating, review count, sentiment)
- Sentiment analysis (TF-IDF + Logistic Regression, lexicon fallback)
- Aspect-based sentiment (keyword + clause rules with negation/contrast)
- Strengths & weaknesses (from aggregated aspect evidence)
- Extractive review summary + keywords
- Review explorer: filter by sentiment/aspect/rating/keyword, sort, paginate
- Natural-language, explainable recommendations (relevance score, not probability)
- Product comparison (2–3 products, table + aspect scores)
- Charts & visualizations (Recharts)

**Advanced (V2)**
- Rating prediction (TF-IDF + Ridge regression)
- Optional transformer sentiment (DistilBERT) — disabled by default, lazy-loaded
- Review authenticity risk (heuristic: duplicates, length, rating/text mismatch)
- Review trend analysis (volume, rating, sentiment, aspect over time)
- Category ranking (confidence-adjusted/Bayesian)
- Personalized recommendations (saved preferences)

**Accounts (V3)**
- Register / login / logout (JWT, bcrypt hashing), protected routes, account settings
- Wishlist, price tracking (demo history), price-drop alerts, in-app notifications
- AI product assistant chatbot (local retrieval, no paid API)

## Tech stack
- **Frontend:** React + Vite, React Router, Recharts, Lucide, hand-crafted olive design system
- **Backend:** Python, FastAPI, Pydantic
- **NLP/ML:** pandas, NumPy, scikit-learn (TF-IDF, LogisticRegression, Ridge, cosine similarity), joblib
- **Auth:** bcrypt, python-jose (JWT)
- **Storage:** MongoDB when reachable, else a local JSON store (automatic fallback)

## Architecture
```
React (Vite)  →  FastAPI REST API  →  ML/NLP (scikit-learn, rules)
                        │
                        └→ Store: MongoDB (optional)  |  local JSON (fallback)
```
`backend/services/analysis_service.py` orchestrates per-product NLP and caches
results. The single-server mode has FastAPI serve the built frontend.

## Project structure
```
backend/    FastAPI app, routes, services, auth, database/store
ml/         NLP/ML modules (sentiment, aspects, summarize, recommend, trends, ranking, fake_review, rating, transformer)
frontend/   React app (pages, components, services)
data/       raw CSV demo data + generator script
models/     trained .pkl artifacts (generated; git-ignored)
api/        Vercel serverless entry (api/index.py)
```

## Setup (Windows)

Requires **Python 3.11** (recommended for ML wheels) and **Node 18+**.

### 1. Backend
```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m ml.train_models      # trains + saves sentiment/rating models
```

### 2. Frontend
```powershell
cd frontend
npm install
cd ..
```

### 3. Environment
```powershell
copy .env.example .env          # adjust values; set a strong JWT_SECRET
```

## Running

### Option A — single server (one URL)
```powershell
python run.py                   # builds frontend, serves everything on 8000
```
App + API: http://localhost:8000  ·  API docs: http://localhost:8000/docs

### Option B — two dev servers (hot reload)
```powershell
# terminal 1
.venv\Scripts\activate; uvicorn backend.main:app --reload --port 8000
# terminal 2
cd frontend; npm run dev
```
Frontend: http://localhost:5173  ·  Backend: http://localhost:8000  ·  Docs: /docs

Or run `./start.ps1` to launch both in separate windows.

## Testing
```powershell
python -m pytest backend/tests -q      # API test suite (TestClient, JSON store)
cd frontend; npm run build             # frontend production build
```

## Database & models
- **MongoDB** is optional. `USE_MONGO=auto` uses it when reachable, else the app
  writes to `data/store/*.json`. The JSON fallback persists across restarts on one
  machine but is not a production database.
- **Models**: `python -m ml.train_models` writes `models/sentiment_model.pkl` and
  `models/rating_model.pkl`. Without them, sentiment falls back to the lexicon.

## Optional transformer (DistilBERT)
Disabled by default to keep startup light.
```powershell
pip install transformers torch
# set ENABLE_TRANSFORMER=1 in .env
```
The baseline TF-IDF model is always active; the transformer is only used when it
actually loads. Status is shown on the Rating page and `/api/analysis/transformer/status`.

## Deployment (Vercel)
`vercel.json` deploys the static frontend plus the FastAPI serverless function
(`api/index.py`). Import the repo on Vercel; no env vars are required for the demo.

> **Limitation:** Vercel serverless functions have a ~250MB size limit. The
> current deps fit, but enabling the transformer (torch) or other heavy ML will
> exceed it — host the backend on a Python platform (Render/Railway) and point the
> frontend at it via `VITE_API_BASE` if you add those.

## Model/data honesty & limitations
- Sentiment labels are **derived from star ratings** (≥4 positive, 3 neutral,
  ≤2 negative). Reported metrics reflect agreement with those weak labels, not
  human-annotated sentiment.
- Aspect sentiment uses keyword + rule heuristics (no large model required).
- Authenticity is a **heuristic risk estimate**, not a trained fraud classifier.
- Price history and alerts run in **demo mode**; there is no live marketplace feed,
  and alerts are evaluated when you open Alerts/Notifications (no external scheduler).
- The chatbot is a **local retrieval assistant**, not an LLM.

## Troubleshooting
- **Port 8000 in use**: stop the other process or run on another port (`--port 8010`).
- **`ModuleNotFoundError: backend`** when running ML scripts: run as a module from
  the repo root, e.g. `python -m ml.train_models`.
- **Sentiment seems weak**: run `python -m ml.train_models` to train the models.
