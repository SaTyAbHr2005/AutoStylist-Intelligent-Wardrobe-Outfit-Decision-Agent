from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class User(BaseModel):
    full_name: str = Field(..., description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    hashed_password: str = Field(..., description="Hashed password")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
