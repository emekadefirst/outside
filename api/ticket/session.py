from bson import ObjectId
from datetime import datetime
from settings.database import db

collection = db["ticket"]




async def create_ticket(
    name, caption, date, time, banner, venue, state, quantity, user_id, unit_price
):
    ticket_data = {
        "name": name,
        "caption": caption,
        "date": date,
        "time": time,
        "venue": venue,
        "state": state,
        "banner": banner,
        "user_id": user_id,
        "quantity": quantity,
        "unit_price": unit_price,
        "created_at": datetime.now(),
    }
    try:
        result = collection.insert_one(ticket_data)
        response = {
            "message": "Ticket created successfully",
            "data": {
                "id": str(result.inserted_id),
                "name": name,
                "caption": caption,
                "date": date,
                "time": time,
                "venue": venue,
                "state": state,
                "quantity": quantity,
                "unit_price": unit_price,
            },
        }
        return response
    except Exception as e:
        return {"error": str(e)}


# if __name__ == "__main__":
#     print(asyncio.run(create_ticket("Victr", "ATM Event", "2025-02-05", "10:00", "banner.jpg", "Venue A", "Lagos", 2, "1234", 5000)))
