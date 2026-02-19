from fastapi import APIRouter, Form
from app.services.context_service import get_weather
from app.config.db import wardrobe_collection
from app.services.decision_engine import generate_ranked_outfits

router = APIRouter()

VALID_OCCASIONS = ["casual", "office", "party", "traditional"]


@router.post("/recommend")
def recommend_outfit(occasion: str = Form(...)):

    if occasion not in VALID_OCCASIONS:
        return {"error": "Invalid occasion"}

    weather = get_weather()

    context = {
        "city": weather["city"],
        "temperature": weather["temperature"],
        "weather": weather["weather"],
        "weather_type": weather["weather_type"],
        "occasion": occasion
    }

    tops = list(wardrobe_collection.find({"category": "top"}))
    bottoms = list(wardrobe_collection.find({"category": "bottom"}))

    if not tops or not bottoms:
        return {"error": "Not enough wardrobe items"}

    ranked_outfits = generate_ranked_outfits(tops, bottoms, context)

    return {
        "context": context,
        "recommendations": {
            "best": {
                "top": ranked_outfits[0]["top"]["image_path"],
                "bottom": ranked_outfits[0]["bottom"]["image_path"],
                "score": ranked_outfits[0]["score"]
            },
            "medium": {
                "top": ranked_outfits[1]["top"]["image_path"],
                "bottom": ranked_outfits[1]["bottom"]["image_path"],
                "score": ranked_outfits[1]["score"]
            } if len(ranked_outfits) > 1 else None,
            "average": {
                "top": ranked_outfits[2]["top"]["image_path"],
                "bottom": ranked_outfits[2]["bottom"]["image_path"],
                "score": ranked_outfits[2]["score"]
            } if len(ranked_outfits) > 2 else None
        }
    }
