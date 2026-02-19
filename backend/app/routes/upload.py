from fastapi import APIRouter, UploadFile, File, Form, HTTPException
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
    gender: str = Form("male"),

    # Optional inputs (used conditionally)
    type: str = Form(None),
    material: str = Form(None)
):

    # -----------------------------------
    # File validation
    # -----------------------------------
    ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG, WEBP images are allowed"
        )

    # -----------------------------------
    # Conditional validation
    # -----------------------------------
    if category in ["accessory", "jewellery"]:
        if not type or not material:
            raise HTTPException(
                status_code=400,
                detail="type and material are required for accessories and jewellery"
            )

    # -----------------------------------
    # Image processing
    # -----------------------------------
    processed_path = process_image(file)

    # -----------------------------------
    # Color extraction
    # -----------------------------------
    colors = extract_dominant_colors(processed_path)

    # Normalize path
    clean_path = processed_path.replace("app/", "")

    # -----------------------------------
    # Prepare DB object (MATCHES WardrobeItem)
    # -----------------------------------
    item = {
        "category": category,
        "style": style,
        "gender": gender,

        "image_path": clean_path,
        "processed_image_path": clean_path,

        "colors": colors,
        "dominant_color": colors[0],
        "color_count": len(colors),

        "preference_score": 0,
        "usage_count": 0,
        "created_at": datetime.utcnow()
    }

    # Add extra metadata only if needed
    if category in ["accessory", "jewellery"]:
        item["type"] = type
        item["material"] = material

    # -----------------------------------
    # Store in MongoDB
    # -----------------------------------
    wardrobe_collection.insert_one(item)

    return {
        "message": "Upload successful",
        "category": category,
        "image_path": item["image_path"],
        "dominant_color": item["dominant_color"]
    }
