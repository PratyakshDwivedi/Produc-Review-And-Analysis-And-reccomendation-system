"""Price alerts.

Alerts are evaluated on demand via check_alerts() (called when alerts or
notifications are fetched). This avoids requiring a long-running background
scheduler. Limitation: without an external scheduler, alerts are only evaluated
when the user is active in the app.
"""
import uuid
from datetime import datetime, timezone

from backend.database.store import get_store
from backend.services import data_loader, notification_service, price_service


def _coll():
    return get_store().collection("alerts")


def create(user_id: str, product_id: str, target_price: float) -> dict:
    if data_loader.get_product(product_id) is None:
        raise ValueError("Product not found")
    alert = {
        "id": uuid.uuid4().hex, "user_id": user_id, "product_id": product_id,
        "target_price": float(target_price), "active": True, "triggered": False,
        "created_at": datetime.now(timezone.utc).isoformat(), "last_triggered": None,
    }
    _coll().insert_one(alert)
    return alert


def list_for(user_id: str) -> list[dict]:
    check_alerts(user_id)
    return _coll().find({"user_id": user_id})


def update(user_id: str, alert_id: str, patch: dict) -> dict | None:
    allowed = {k: patch[k] for k in ("target_price", "active") if k in patch}
    return _coll().update_one({"user_id": user_id, "id": alert_id}, allowed)


def delete(user_id: str, alert_id: str) -> int:
    return _coll().delete_one({"user_id": user_id, "id": alert_id})


def check_alerts(user_id: str) -> list[dict]:
    """Evaluate active alerts; create a notification when price <= target."""
    triggered = []
    for alert in _coll().find({"user_id": user_id, "active": True}):
        price = price_service.current_price(alert["product_id"])
        if price is None:
            continue
        if price <= alert["target_price"] and not alert.get("triggered"):
            product = data_loader.get_product(alert["product_id"])
            notification_service.create(
                user_id,
                f"Price alert: {product['name']} is now ${price} (target ${int(alert['target_price'])}).",
                kind="price_alert", meta={"product_id": alert["product_id"], "price": price},
            )
            _coll().update_one(
                {"user_id": user_id, "id": alert["id"]},
                {"triggered": True, "last_triggered": datetime.now(timezone.utc).isoformat()},
            )
            triggered.append(alert["id"])
        elif price > alert["target_price"] and alert.get("triggered"):
            _coll().update_one({"user_id": user_id, "id": alert["id"]}, {"triggered": False})
    return triggered
