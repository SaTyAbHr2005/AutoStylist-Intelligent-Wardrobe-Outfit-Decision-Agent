from fastapi import APIRouter, Form
from app.services.context_service import get_weather
from app.config.db import wardrobe_collection
from app.services.decision_engine import generate_ranked_outfits
from app.services.accessories_engine import (
    select_best_shoes,
    select_accessories,
    select_jewellery
)

router = APIRouter()

VALID_OCCASIONS = ["casual", "office", "party", "traditional"]


@router.post("/recommend")
def recommend_outfit(occasion: str = Form(...)):

    # -----------------------------
    # Validate input
    # -----------------------------
    if occasion not in VALID_OCCASIONS:
        return {"error": "Invalid occasion"}

    # -----------------------------
    # Module 2 — Context
    # -----------------------------
    weather = get_weather()

    context = {
        "city": weather.get("city", "Unknown"),
        "temperature": weather.get("temperature"),
        "weather": weather.get("weather"),
        "weather_type": weather.get("weather_type", "normal"),
        "occasion": occasion
    }

    # -----------------------------
    # Style mapping for filtering
    # -----------------------------
    style_map = {
        "casual": "casual",
        "office": "formal",
        "party": "party",
        "traditional": "traditional"
    }

    style_filter = style_map.get(occasion, "casual")

    # -----------------------------
    # Fetch wardrobe data
    # -----------------------------
    tops = list(wardrobe_collection.find({
        "category": "top",
        "style": style_filter
    }))

    bottoms = list(wardrobe_collection.find({
        "category": "bottom",
        "style": style_filter
    }))

    shoes = list(wardrobe_collection.find({
        "category": "shoes"
    }))

    accessories = list(wardrobe_collection.find({
        "category": "accessories"
    }))

    jewellery = list(wardrobe_collection.find({
        "category": "jewellery"
    }))

    if not tops or not bottoms:
        return {"error": "Not enough wardrobe items for this occasion"}

    # -----------------------------
    # Module 3 — Outfit Decision
    # -----------------------------
    ranked_outfits = generate_ranked_outfits(tops, bottoms, context)

    if not ranked_outfits:
        return {"error": "No suitable outfit found"}

    # Top 3 recommendations
    best = ranked_outfits[0]
    medium = ranked_outfits[1] if len(ranked_outfits) > 1 else None
    average = ranked_outfits[2] if len(ranked_outfits) > 2 else None

    # -----------------------------
    # Module 4 — Extras based on BEST
    # -----------------------------
    selected_shoes = select_best_shoes(shoes, best, context)
    selected_accessories = select_accessories(accessories, occasion)
    selected_jewellery = select_jewellery(jewellery, occasion)

    # -----------------------------
    # Response Formatter
    # -----------------------------
    def format_outfit(outfit):
        if not outfit:
            return None
        return {
            "top": outfit["top"].get("image_path"),
            "bottom": outfit["bottom"].get("image_path"),
            "score": outfit["score"]
        }

    return {
        "context": context,
        "recommendations": {
            "best": format_outfit(best),
            "medium": format_outfit(medium),
            "average": format_outfit(average)
        },
        "extras": {
            "shoes": (
                selected_shoes.get("image_path")
                if selected_shoes else None
            ),
            "accessories": [
                item.get("image_path")
                for item in selected_accessories
            ] if selected_accessories else [],
            "jewellery": (
                selected_jewellery.get("image_path")
                if selected_jewellery else None
            )
        }
    }
