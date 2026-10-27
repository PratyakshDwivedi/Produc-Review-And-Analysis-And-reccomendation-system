"""End-to-end API tests (FastAPI TestClient, JSON store in a temp dir)."""
import os
import tempfile

os.environ["USE_MONGO"] = "0"
os.environ["STORE_DIR"] = tempfile.mkdtemp(prefix="pra_store_")

from fastapi.testclient import TestClient  # noqa: E402

from backend.main import app  # noqa: E402

client = TestClient(app)


def _first_product_id():
    return client.get("/api/products").json()[0]["product_id"]


def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_products_and_search():
    assert len(client.get("/api/products").json()) >= 10
    assert all("smartphone" == p["category"] for p in client.get("/api/products?category=smartphone").json())
    assert len(client.get("/api/products?q=nova").json()) >= 1
    assert client.get("/api/products/NOPE").status_code == 404


def test_analysis_endpoints():
    pid = _first_product_id()
    a = client.get(f"/api/analysis/{pid}").json()
    assert "sentiment_distribution" in a and a["aspects"]
    assert set(client.get(f"/api/analysis/{pid}/sentiment").json()["distribution"]) == {"positive", "neutral", "negative"}
    assert "strengths" in client.get(f"/api/analysis/{pid}/aspects").json()
    assert "summary" in client.get(f"/api/analysis/{pid}/summary").json()
    assert client.get(f"/api/analysis/{pid}/trends").json()["available"] is True
    assert "flagged_count" in client.get(f"/api/analysis/{pid}/authenticity").json()


def test_reviews_filtering():
    pid = _first_product_id()
    r = client.get(f"/api/reviews/{pid}?sentiment=positive&page_size=5").json()
    assert r["page_size"] == 5
    assert all(x["sentiment"] == "positive" for x in r["items"])


def test_recommend_and_rank():
    rec = client.post("/api/recommend", json={"query": "phone with great camera and gaming under $800"}).json()
    assert rec["results"] and rec["parsed"]["budget"] == 800
    rk = client.get("/api/rankings?category=smartphone").json()
    assert rk["ranking"][0]["rank"] == 1


def test_compare_and_rating():
    ids = ",".join(p["product_id"] for p in client.get("/api/products?category=smartphone").json()[:2])
    assert len(client.get(f"/api/compare?ids={ids}").json()["products"]) == 2
    pr = client.post("/api/analysis/predict-rating", json={"text": "excellent camera and battery"}).json()
    assert pr["predicted_rating"] is not None


def test_auth_wishlist_alerts_flow():
    email = f"t{os.getpid()}@example.com"
    reg = client.post("/api/auth/register", json={"email": email, "password": "secret1", "name": "T"})
    assert reg.status_code == 201
    token = reg.json()["token"]
    h = {"Authorization": f"Bearer {token}"}
    assert client.get("/api/auth/me", headers=h).json()["email"] == email
    assert client.get("/api/wishlist").status_code == 401  # protected

    pid = _first_product_id()
    client.post("/api/wishlist", json={"product_id": pid}, headers=h)
    client.post("/api/wishlist", json={"product_id": pid}, headers=h)  # dedup
    assert len(client.get("/api/wishlist", headers=h).json()) == 1

    client.put("/api/preferences", json={"category": "smartphone", "budget": 700,
                                         "preferred_aspects": ["camera"], "min_rating": 4}, headers=h)
    assert client.get("/api/preferences", headers=h).json()["budget"] == 700

    # alert that triggers immediately (target above current price)
    high = client.get(f"/api/price/{pid}").json()["current_price"] + 100
    client.post("/api/alerts", json={"product_id": pid, "target_price": high}, headers=h)
    notes = client.get("/api/notifications", headers=h).json()
    assert notes["unread"] >= 1


def test_chatbot():
    r = client.post("/api/chat", json={"message": "Which phone has the best camera?"}).json()
    assert "reply" in r and len(r["reply"]) > 0
