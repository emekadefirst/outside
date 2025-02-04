from bson import ObjectId
from datetime import datetime
from settings.database import db

collection = db["users"]


async def create_user(username, email, password):
    applicant_data = {
        "username": username,
        "email": email,
        "role": "user",
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
            },
        }
        return response
    except Exception as e:
        return {"error": str(e)}


# if __name__ == "__main__":
#     # print(asyncio.run(create_user("victr", "atm@s.com", "dahbsdas")))
#     print(asyncio.run(get_user("67a0ba231c0d523f9b90545f")))
