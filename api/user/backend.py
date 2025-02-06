import os
import jwt
import asyncio
from dotenv import load_dotenv
from typing import Annotated
from bson import ObjectId
from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from .sessions import collection

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_TIME = timedelta(days=30)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        raise ValueError("Unknown password hash format!", e)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(user_id: str):
    try:
        user = collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise "User not found"

        user_data = {
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "password": user["password"],
            "created_at": user["created_at"],
        }
        return {"message": "User retrieved successfully", "data": user_data}

    except Exception as e:
        raise f"Error retrieving user: {str(e)}"


def authenticate_user(password: str, email: str):
    if not email:
        raise ValueError("Email must be provided for authentication.")

    user = collection.find_one({"email": email})
    if not user:
        return None  # No user found with the given email
    if "password" not in user:
        raise ValueError("Stored user has no password field!")

    if not verify_password(password, user["password"]):
        return None  # Wrong password

    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "role": user["role"],
        "created_at": user["created_at"].isoformat(),
    }


