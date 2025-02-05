from fastapi import APIRouter, Form, UploadFile, File, HTTPException, status
from .session import create_ticket, collection
from services.cloud import cloud
from fastapi.responses import JSONResponse
from settings.decorators import role_required
from bson import ObjectId
from fastapi import HTTPException

ticket = APIRouter()


@ticket.post("/tickets/create")
# @role_required(allowed_roles=["ADMIN", "HOST"])
async def create_ticket_endpoint(
    name: str = Form(...),
    caption: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    address: str = Form(...),
    state: str = Form(...),
    user_id: str = Form(...),
    quantity: int = Form(...),
    unit_price: float = Form(...),
    banner: UploadFile = File(...),
):

    file_content = await banner.read()
    banner_url = cloud(file_content, name)
    try:
        ticket_response = await create_ticket(
            name=name,
            caption=caption,
            date=date,
            time=time,
            venue=address,  # Ensure correct parameter
            state=state,
            quantity=quantity,
            user_id=user_id,
            unit_price=unit_price,
            banner=banner_url,
        )
        content = {
            "message": "Ticket created successfully",
            "ticket_id": ticket_response["data"]["id"],
            "name": name,
            "caption": caption,
            "banner": banner_url,
        }

        return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ticket creation failed: {str(e)}")


@ticket.get("/tickets/")
async def get_all_tickets():
    try:
        tickets = collection.find()
        tickets_list = list(tickets)
        for ticket in tickets_list:
            ticket["_id"] = str(ticket["_id"])
        return {"tickets": tickets_list}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch tickets: {str(e)}"
        )


@ticket.get("/tickets/{id}")
async def get_ticket_by_id(id: str):
    try:
        ticket = collection.find_one({"_id": ObjectId(id)})  # Convert string ID to ObjectId
        if ticket:
            ticket["_id"] = str(ticket["_id"])  # Convert ObjectId back to string for response
            return {"ticket": ticket}
        else:
            raise HTTPException(status_code=404, detail="Ticket not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch ticket: {str(e)}")

@ticket.delete("/tickets/{id}")
async def delete_ticket(id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Ticket not found")

        return {"message": "Ticket deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete ticket: {str(e)}")


@ticket.patch("/tickets/{id}")
async def update_ticket(id: str, updated_data: dict):
    try:
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Ticket not found")

        return {"message": "Ticket updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update ticket: {str(e)}")
