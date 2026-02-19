from fastapi import APIRouter, Form
from app.services.context_service import get_weather
from app.config.db import wardrobe_collection
from app.services.decision_engine import generate_ranked_outfits
from app.services.accessory_engine import select_accessories, select_jewellery

router = APIRouter()

VALID_OCCASIONS = ["casual", "office", "party", "traditional"]


@router.post("/recommend")
def recommend_outfit(occasion: str = Form(...), gender: str = Form("male")):

    # ----------------------------
    # Validate input
    # ----------------------------
    if occasion not in VALID_OCCASIONS:
        return {"error": "Invalid occasion"}

    # ----------------------------
    # Context (Module 2)
    # ----------------------------
    weather = get_weather()

    context = {
        "city": weather["city"],
        "temperature": weather["temperature"],
        "weather": weather["weather"],
        "weather_type": weather["weather_type"],
        "occasion": occasion
    }

    # ----------------------------
    # Fetch wardrobe items
    # ----------------------------
    tops = list(wardrobe_collection.find({"category": "top", "gender": gender}))
    bottoms = list(wardrobe_collection.find({"category": "bottom", "gender": gender}))
    accessories = list(wardrobe_collection.find({"category": "accessory", "gender": gender}))
    jewellery = list(wardrobe_collection.find({"category": "jewellery", "gender": gender}))

    if not tops or not bottoms:
        return {"error": "Not enough wardrobe items"}

    # ----------------------------
    # Outfit decision (Module 3)
    # ----------------------------
    ranked = generate_ranked_outfits(tops, bottoms, context)

    if not ranked or "best" not in ranked:
        return {"error": "Could not generate recommendations"}

    # ----------------------------
    # Accessory refinement (Module 4)
    # ----------------------------
    final_output = {}

    for label in ["best", "average"]:
        if label not in ranked:
            continue

        outfit = ranked[label]

        final_output[label] = {
            "top": outfit["top"]["image_path"],
            "bottom": outfit["bottom"]["image_path"],
            "score": outfit["score"],

            "accessories": [
                a["image_path"]
                for a in select_accessories(
                    outfit,
                    accessories,
                    occasion,
                    context["weather_type"]
                )
            ],

            "jewellery": [
                j["image_path"]
                for j in select_jewellery(
                    outfit,
                    jewellery,
                    occasion
                )
            ]
        }

    # ----------------------------
    # Final response
    # ----------------------------
    return {
        "context": context,
        "recommendations": final_output
    }
