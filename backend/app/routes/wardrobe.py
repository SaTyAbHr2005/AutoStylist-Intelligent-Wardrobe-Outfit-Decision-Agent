from fastapi import APIRouter, Depends, HTTPException
from app.config.db import wardrobe_collection
from app.services.auth_service import get_current_user
from typing import List

router = APIRouter()

@router.get("/wardrobe")
def get_wardrobe(current_user: dict = Depends(get_current_user)):
    """Fetch all wardrobe items for the current user."""
    items_cursor = wardrobe_collection.find({"user_id": str(current_user["_id"])})
    items = []
    for doc in items_cursor:
        doc["_id"] = str(doc["_id"])
        items.append(doc)
    return {"items": items}

@router.get("/wardrobe/{category}")
def get_wardrobe_by_category(category: str, current_user: dict = Depends(get_current_user)):
    """Fetch wardrobe items by category for the current user."""
    items_cursor = wardrobe_collection.find({
        "user_id": str(current_user["_id"]),
        "category": category
    })
    items = []
    for doc in items_cursor:
        doc["_id"] = str(doc["_id"])
        items.append(doc)
    return {"items": items}

@router.get("/stats")
def get_wardrobe_stats(current_user: dict = Depends(get_current_user)):
    """Fetch wardrobe statistics for the current user."""
    pipeline = [
        {"$match": {"user_id": str(current_user["_id"])}},
        {"$group": {"_id": "$category", "count": {"$sum": 1}}}
    ]
    stats_cursor = wardrobe_collection.aggregate(pipeline)
    
    # We also want total items
    total_items = wardrobe_collection.count_documents({"user_id": str(current_user["_id"])})
    
    category_counts = {}
    for stat in stats_cursor:
        category_counts[stat["_id"]] = stat["count"]
        
    return {
        "total": total_items,
        "categories": category_counts
    }

@router.delete("/wardrobe/{item_id}")
def delete_wardrobe_item(item_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a wardrobe item for the current user."""
    from bson.objectid import ObjectId
    try:
        result = wardrobe_collection.delete_one({
            "_id": ObjectId(item_id),
            "user_id": str(current_user["_id"])
        })
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Item not found or unauthorized")
        return {"message": "Item deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid item ID")
