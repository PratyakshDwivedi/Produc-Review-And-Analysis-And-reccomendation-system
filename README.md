# Product Review Analysis & Recommendation System

AI/NLP-powered system that analyzes product reviews and produces sentiment,
aspect-based insights, summaries, and explainable recommendations.

## Stack
- **Frontend:** React (Vite), Recharts
- **Backend:** Python, FastAPI (REST)
- **NLP/ML:** pandas, NLTK, spaCy, scikit-learn (added in later phases)
- **Database:** MongoDB (integrated in a later phase; CSV is the Phase 1 source)

## Project status
Built incrementally in phases. Phase 1 (project setup, dataset, and the
frontend ↔ backend connection) is complete.

## Setup

### Backend
```bash
py -3.11 -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
uvicorn backend.main:app --reload
```
API runs at http://127.0.0.1:8000 (docs at /docs).

### Frontend
```bash
cd frontend
npm install
npm run dev
```
App runs at http://localhost:5173.

### Environment
Copy `.env.example` to `.env` and adjust values. Secrets are never committed.

## Phase 1 endpoints
- `GET /health` — service + MongoDB status
- `GET /api/products` — list products (`?q=` to search by name)
- `GET /api/products/{id}` — single product
- `GET /api/reviews/{product_id}` — reviews for a product
