from fastapi import APIRouter, UploadFile, File, Form
from datetime import datetime

from app.services.image_service import process_image
from app.services.color_service import extract_dominant_colors
from app.config.db import wardrobe_collection

router = APIRouter()


@router.post("/upload")
async def upload_item(
    file: UploadFile = File(...),
    category: str = Form(...),
    style: str = Form("casual"),
    gender: str = Form("male")
):

    ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]

    if file.content_type not in ALLOWED_TYPES:
        return {"error": "Only JPG, PNG, WEBP allowed"}

    # Process image
    processed_path = process_image(file)

    # Extract colors
    colors = extract_dominant_colors(processed_path)
    
    # Store in DB

    item = {
        "category": category,
        "style": style,
        "gender": gender,
        "colors": colors,
        "dominant_color": colors[0],
        "color_count": len(colors),
        "image_path": processed_path.replace("app/", ""),
        "preference_score": 0,
        "usage_count": 0,
    }

    wardrobe_collection.insert_one(item)

    return {
        "message": "Upload successful",
        "colors": colors,
        "image": item["image_path"]
    }
