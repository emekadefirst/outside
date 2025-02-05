from fastapi import APIRouter, status, HTTPException
from .sessions import create_user, collection
from fastapi.responses import JSONResponse
from .valdidator import UserSignup, UserLogin
from bson import ObjectId
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

@auth.get("/users")
async def get_users():
    try:
        users = collection.find()
        users_list = list(users)
        for user in users_list:
            user["_id"] = str(user["_id"])
        return {"users": users_list}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch users: {str(e)}"
        )


@auth.get("/users/{id}")
async def get_user_by_id(id: str):
    try:
        user = collection.find_one({"_id": ObjectId(id)}) 
        if user:
            user["_id"] = str(user["_id"])  
            return {"user": user}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user: {str(e)}")


@auth.delete("/users/{id}")
async def delete_user(id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete user: {str(e)}"
        )


@auth.patch("/users/{id}")
async def update_user(id: str, updated_data: dict):
    try:
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update ticket: {str(e)}"
        )
