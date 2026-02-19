from fastapi import APIRouter, Form
from datetime import datetime
from app.config.db import wardrobe_collection

router = APIRouter()

MAX_PREF = 5
MIN_PREF = -5


# -------------------------------------------------
# Preference Update Helper
# -------------------------------------------------
def update_preference(image_path, change):
    item = wardrobe_collection.find_one({"image_path": image_path})
    if not item:
        return

    current_score = item.get("preference_score", 0)
    new_score = current_score + change

    # Clamp between -5 and +5
    new_score = max(MIN_PREF, min(MAX_PREF, new_score))

    wardrobe_collection.update_one(
        {"image_path": image_path},
        {"$set": {"preference_score": new_score}}
    )


def update_usage(image_path):
    wardrobe_collection.update_one(
        {"image_path": image_path},
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
    selected_top: str = Form(...),
    selected_bottom: str = Form(...),

    medium_top: str = Form(...),
    medium_bottom: str = Form(...),

    average_top: str = Form(...),
    average_bottom: str = Form(...),

    action: str = Form(...)
):
    """
    action = like | dislike | wear
    """

    if action not in ["like", "dislike", "wear"]:
        return {"error": "Invalid action"}

    # Selected outfit
    selected = [(selected_top, selected_bottom)]

    # Other outfits
    others = [
        (medium_top, medium_bottom),
        (average_top, average_bottom)
    ]

    # -------------------------------------------------
    # Like / Dislike (Relative Learning)
    # -------------------------------------------------
    if action == "like":
        selected_change = 1
        others_change = -1

    elif action == "dislike":
        selected_change = -1
        others_change = 1

    # -------------------------------------------------
    # Apply Preference Changes
    # -------------------------------------------------
    if action in ["like", "dislike"]:
        # Update selected
        for top, bottom in selected:
            update_preference(top, selected_change)
            update_preference(bottom, selected_change)

        # Update others
        for top, bottom in others:
            update_preference(top, others_change)
            update_preference(bottom, others_change)

    # -------------------------------------------------
    # Wear Action
    # -------------------------------------------------
    if action == "wear":
        update_usage(selected_top)
        update_usage(selected_bottom)

    return {"message": "Relative feedback recorded"}
