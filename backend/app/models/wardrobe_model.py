from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class WardrobeItem(BaseModel):
    category: str = Field(
        ...,
        description="top | bottom | shoes | accessories | jewellery"
    )

    style: str = Field(
        default="casual",
        description="casual | formal | party | traditional"
    )

    # Image
    image_path: str

    # Color information
    colors: List[List[int]] = Field(
        description="List of RGB colors"
    )
    dominant_color: List[int] = Field(
        description="Primary RGB color"
    )
    color_count: int

    # Accessory / Jewellery metadata
    type: Optional[str] = Field(
        default=None,
        description="watch, belt, ring, necklace, etc."
    )
    material: Optional[str] = Field(
        default=None,
        description="metal, leather, fabric, gold, etc."
    )

    # Learning & tracking
    preference_score: int = Field(
        default=0,
        description="User preference score (-5 to +5)"
    )
    usage_count: int = 0
    last_used: Optional[datetime] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "category": "accessories",
                "style": "casual",
                "image_path": "static/processed/silver_watch.png",
                "colors": [[192, 192, 192]],
                "dominant_color": [192, 192, 192],
                "color_count": 1,
                "type": "watch",
                "material": "metal",
                "preference_score": 0,
                "usage_count": 0
            }
        }
