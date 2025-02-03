import os
import asyncio
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId


# Load environment variables
load_dotenv()

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)

db = client["User"]
print("✅ Connected to MongoDB successfully!")
collection = db["users"]


async def create_user(username, email, password):
    applicant_data = {
        "username": username,
        "email": email,
        "role": "user",
        "is_host": False,
        "password": password,
        "created_at": datetime.now(),
    }
    try:
        result = collection.insert_one(applicant_data)
        response = {
            "message": "User created successfully",
            "data": {
                "id": str(result.inserted_id),  
                "username": username,
                "email": email,
                "role": "user", 
                "is_host": False,
            },
        }
        return response
    except Exception as e:
        return {"error": str(e)}  

# if __name__ == "__main__":
#     # print(asyncio.run(create_user("victr", "atm@s.com", "dahbsdas")))
#     print(asyncio.run(get_user("67a0ba231c0d523f9b90545f")))
