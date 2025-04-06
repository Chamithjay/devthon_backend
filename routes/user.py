from fastapi import APIRouter, HTTPException

from database import get_user_collection
from models.user import Token, UserCreate, UserResponse
from utils.auth import create_access_token, verify_access_token
from utils.deps import hash_password, verify_password

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    users_collection = get_user_collection()
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    user_dict = {"name": user.name, "email": user.email, "password": hashed_password}
    result = await users_collection.insert_one(user_dict)
    return {"id": str(result.inserted_id), "name": user.name, "email": user.email}


@router.post("/login", response_model=Token)
async def login_user(user: UserCreate):
    users_collection = get_user_collection()
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"user_id": str(db_user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/protected")
async def protected_route(token: str):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"message": "Access granted!", "user_id": payload["user_id"]}
