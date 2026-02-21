from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user_model import UserCreate, UserLogin, User, Token
from app.services.auth_service import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    oauth2_scheme
)
from app.config.db import users_collection, token_blocklist_collection
from datetime import timedelta, datetime
import jwt

router = APIRouter()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = {
        "full_name": user.full_name,
        "email": user.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }

    result = users_collection.insert_one(new_user)
    new_user["_id"] = result.inserted_id
    
    return User(**new_user)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        valid = verify_password(form_data.password, user.get("hashed_password", ""))
    except Exception as e:
        # avoid exposing internals
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "user_id": str(user["_id"])}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme), current_user: dict = Depends(get_current_user)):
    """
    Invalidates the current JWT token by adding it to the blocklist.
    Requests MUST include a valid Authorization Bearer token to log out.
    """
    token_blocklist_collection.insert_one({
        "token": token,
        "user_id": str(current_user["_id"]),
        "blocklisted_at": datetime.utcnow()
    })
    
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=User)
def get_me(current_user: dict = Depends(get_current_user)):
    return User(**current_user)
