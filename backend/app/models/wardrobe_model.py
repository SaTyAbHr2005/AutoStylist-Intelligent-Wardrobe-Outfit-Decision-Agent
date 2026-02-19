from pydantic import BaseModel
from typing import List, Optional

class WardrobeItem(BaseModel):
    name: str
    category: str
    colors: List[str]
    image_url: str
    processed_image_url: Optional[str] = None
