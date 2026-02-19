from fastapi import APIRouter, Form
from app.services.context_service import get_weather

router = APIRouter()

VALID_OCCASIONS = ["casual", "office", "party", "traditional"]


@router.post("/context")
def get_context(occasion: str = Form(...)):
    if occasion not in VALID_OCCASIONS:
        return {"error": "Invalid occasion"}

    weather_data = get_weather()

    context = {
        "city": weather_data["city"],
        "temperature": weather_data["temperature"],
        "weather": weather_data["weather"],
        "weather_type": weather_data["weather_type"],
        "occasion": occasion
    }

    return context
