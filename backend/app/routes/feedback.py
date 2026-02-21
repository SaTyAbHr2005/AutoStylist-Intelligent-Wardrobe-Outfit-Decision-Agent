from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from bson.objectid import ObjectId
from app.config.db import wardrobe_collection
from app.services.auth_service import get_current_user

router = APIRouter()

MAX_PREF = 5
MIN_PREF = -5

class FeedbackPayload(BaseModel):
    liked_items: List[str]
    disliked_items: List[str]
    worn_items: List[str]


# -------------------------------------------------
# Preference Update Helper
# -------------------------------------------------
def update_preference(item_id: str, change: int, user_id: str):
    if not item_id:
        return
        
    try:
        obj_id = ObjectId(item_id)
    except:
        return

    item = wardrobe_collection.find_one({"_id": obj_id, "user_id": user_id})
    if not item:
        return

    current_score = item.get("preference_score", 0)
    new_score = current_score + change

    # Clamp between -5 and +5
    new_score = max(MIN_PREF, min(MAX_PREF, new_score))

    wardrobe_collection.update_one(
        {"_id": obj_id, "user_id": user_id},
        {"$set": {"preference_score": new_score}}
    )


def update_usage(item_id: str, user_id: str):
    if not item_id:
        return
        
    try:
        obj_id = ObjectId(item_id)
    except:
        return
        
    wardrobe_collection.update_one(
        {"_id": obj_id, "user_id": user_id},
        {
            "$inc": {"usage_count": 1},
            "$set": {"last_used": datetime.utcnow()}
        }
    )


# -------------------------------------------------
# Feedback Route
# -------------------------------------------------
@router.post("/feedback")
def feedback(
    payload: FeedbackPayload,
    current_user: dict = Depends(get_current_user)
):
    """
    Apply +1 to liked_items, -1 to disliked_items, and update usage for worn_items
    """
    user_id_str = str(current_user["_id"])

    # 1. Process Liked items (+1 preference)
    for item_id in payload.liked_items:
        update_preference(item_id, 1, user_id_str)

    # 2. Process Disliked items (-1 preference)
    for item_id in payload.disliked_items:
        update_preference(item_id, -1, user_id_str)

    # 3. Process Worn items (increment usage)
    for item_id in payload.worn_items:
        update_usage(item_id, user_id_str)

    return {"message": "Feedback safely recorded using IDs"}
