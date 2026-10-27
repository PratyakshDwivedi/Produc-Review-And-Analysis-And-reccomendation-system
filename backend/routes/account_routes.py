"""Account features: wishlist, preferences, price tracking, alerts, notifications."""
from fastapi import APIRouter, Depends, HTTPException

from backend import schemas
from backend.auth.dependencies import get_current_user
from backend.services import (
    alert_service, notification_service, preference_service, price_service,
    wishlist_service,
)

router = APIRouter(prefix="/api", tags=["account"])


# ---- wishlist ----
@router.get("/wishlist")
def get_wishlist(user=Depends(get_current_user)):
    return wishlist_service.list_items(user["id"])


@router.post("/wishlist")
def add_wishlist(req: schemas.WishlistRequest, user=Depends(get_current_user)):
    try:
        return wishlist_service.add(user["id"], req.product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/wishlist/{product_id}")
def remove_wishlist(product_id: str, user=Depends(get_current_user)):
    return wishlist_service.remove(user["id"], product_id)


# ---- preferences ----
@router.get("/preferences")
def get_prefs(user=Depends(get_current_user)):
    return preference_service.get_preferences(user["id"])


@router.put("/preferences")
def set_prefs(req: schemas.PreferencesRequest, user=Depends(get_current_user)):
    return preference_service.set_preferences(user["id"], req.model_dump())


# ---- price tracking (history is public; recording requires auth) ----
@router.get("/price/{product_id}")
def price_history(product_id: str):
    h = price_service.history(product_id)
    if not h:
        raise HTTPException(status_code=404, detail="Product not found")
    return h


@router.post("/price")
def record_price(req: schemas.PriceRecord, user=Depends(get_current_user)):
    try:
        return price_service.record_price(req.product_id, req.price)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ---- alerts ----
@router.get("/alerts")
def list_alerts(user=Depends(get_current_user)):
    return alert_service.list_for(user["id"])


@router.post("/alerts", status_code=201)
def create_alert(req: schemas.AlertCreate, user=Depends(get_current_user)):
    try:
        alert = alert_service.create(user["id"], req.product_id, req.target_price)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    alert_service.check_alerts(user["id"])
    return alert


@router.put("/alerts/{alert_id}")
def update_alert(alert_id: str, req: schemas.AlertUpdate, user=Depends(get_current_user)):
    updated = alert_service.update(user["id"], alert_id, req.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Alert not found")
    return updated


@router.delete("/alerts/{alert_id}")
def delete_alert(alert_id: str, user=Depends(get_current_user)):
    removed = alert_service.delete(user["id"], alert_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"removed": alert_id}


# ---- notifications ----
@router.get("/notifications")
def list_notifications(user=Depends(get_current_user)):
    alert_service.check_alerts(user["id"])
    return {"items": notification_service.list_for(user["id"]),
            "unread": notification_service.unread_count(user["id"])}


@router.post("/notifications/{notification_id}/read")
def read_notification(notification_id: str, user=Depends(get_current_user)):
    updated = notification_service.mark_read(user["id"], notification_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated


@router.post("/notifications/read-all")
def read_all(user=Depends(get_current_user)):
    return {"marked": notification_service.mark_all_read(user["id"])}
