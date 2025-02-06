import os
import asyncio
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)

db = client["OutsideCluster"]

collection = db["users"]
async def get_user(user_id: str):
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

# print(asyncio.run(get_user("67a3a98e99c59a570ed911d1")))
