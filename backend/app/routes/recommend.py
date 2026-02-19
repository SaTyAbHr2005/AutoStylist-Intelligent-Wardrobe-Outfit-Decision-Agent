from fastapi import APIRouter, Form
from app.services.context_service import get_weather
from app.config.db import wardrobe_collection

router = APIRouter()

VALID_OCCASIONS = ["casual", "office", "party", "traditional"]


@router.post("/recommend")
def recommend_outfit(occasion: str = Form(...)):
    # Validate occasion
    if occasion not in VALID_OCCASIONS:
        return {"error": "Invalid occasion"}

    # Step 1: Get weather context
    weather_data = get_weather()

    context = {
        "city": weather_data["city"],
        "temperature": weather_data["temperature"],
        "weather": weather_data["weather"],
        "weather_type": weather_data["weather_type"],
        "occasion": occasion
    }

    # Step 2: Filter wardrobe based on occasion
    # (simple logic for now)

    if occasion == "office":
        style_filter = "formal"
    elif occasion == "party":
        style_filter = "party"
    elif occasion == "traditional":
        style_filter = "traditional"
    else:
        style_filter = "casual"

    tops = list(wardrobe_collection.find({
        "category": "top",
        "style": style_filter
    }))

    bottoms = list(wardrobe_collection.find({
        "category": "bottom",
        "style": style_filter
    }))

    shoes = list(wardrobe_collection.find({
        "category": "shoes",
        "style": style_filter
    }))

    # Step 3: Simple combination (first available)
    if not tops or not bottoms:
        return {"error": "Not enough wardrobe items for this occasion"}

    outfit = {
        "top": tops[0]["image_path"],
        "bottom": bottoms[0]["image_path"],
        "shoes": shoes[0]["image_path"] if shoes else None
    }

    return {
        "context": context,
        "outfit": outfit
    }
