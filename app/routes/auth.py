from fastapi import APIRouter, HTTPException,Depends
from datetime import datetime
from uuid import uuid4

from ..db import db
from ..models import UserCreate, UserOut, Token
from ..utils import hash_password, verify_password, create_access_token
from ..dependency  import get_current_user


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=dict)
async def signup(user: UserCreate):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = {
        "id": str(uuid4()),
        "email": user.email,
        "hashed_password": hash_password(user.password),
        "created_at": datetime.utcnow()
    }
    await db.users.insert_one(user_dict)
    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
async def login(user: UserCreate):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"user_id": db_user["id"]})
    return {"access_token": token}

@router.get("/me", response_model=UserOut)
async def get_me(current_user:UserOut = Depends(get_current_user)):  # Replaced in `main.py`
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "created_at": current_user["created_at"]
    }
