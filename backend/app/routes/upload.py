from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
import os
import shutil
import uuid
from datetime import datetime
import cloudinary
import cloudinary.uploader

from app.services.image_service import process_image
from app.services.color_service import extract_dominant_colors
from app.config.db import wardrobe_collection
from app.services.auth_service import get_current_user

# Configure Cloudinary globally or here
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

router = APIRouter()


@router.post("/upload")
async def upload_item(
    file: UploadFile = File(...),
    category: str = Form(...),
    style: str = Form("casual"),
    gender: str = Form("male"),
    current_user: dict = Depends(get_current_user)
):

    ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]

    if file.content_type not in ALLOWED_TYPES:
        return {"error": "Only JPG, PNG, WEBP allowed"}

    # The existing image_service logic saves locally, which is fine temporarily 
    # for background removal or we can push the raw file direct.
    # Assuming `process_image` removes background and saves a local file.
    processed_path = process_image(file)

    # Extract colors from the local processed file
    colors = extract_dominant_colors(processed_path)
    
    # Upload to Cloudinary
    try:
        upload_result = cloudinary.uploader.upload(processed_path, folder="autostylist_wardrobe")
        cloudinary_url = upload_result.get("secure_url")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloudinary upload failed: {str(e)}")
        
    # Optional: Clean up the local processed file if we no longer need it.
    if os.path.exists(processed_path):
        os.remove(processed_path)

    # Store in DB
    item = {
        "user_id": str(current_user["_id"]),
        "category": category,
        "style": style,
        "gender": gender,
        "colors": colors,
        "dominant_color": colors[0],
        "color_count": len(colors),
        "image_path": cloudinary_url,
        "preference_score": 0,
        "usage_count": 0,
        "created_at": datetime.utcnow()
    }

    wardrobe_collection.insert_one(item)

    return {
        "message": "Upload successful",
        "colors": colors,
        "image": item["image_path"]
    }
