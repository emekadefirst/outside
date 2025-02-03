from fastapi import APIRouter, status, HTTPException
from .database import create_user
from fastapi.responses import JSONResponse
from .valdidator import UserSignup, UserLogin
from .backend import create_access_token, authenticate_user, get_password_hash

auth = APIRouter()

@auth.post("user/auth/login")
async def login_user(data: UserLogin):
    user_data = authenticate_user(email=data.email, password=data.password)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": user_data["id"]})  # Now user_data is a dictionary
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": access_token, "data": user_data},
    )


@auth.post("user/auth/signup")
async def signup_user(user: UserSignup):
    user_data = await create_user(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    access_token = create_access_token({"sub": user_data["data"]["id"]})
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"access_token": access_token, "data": user_data}
    )
