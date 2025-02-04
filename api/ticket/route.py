from fastapi import APIRouter, Form, UploadFile, File, HTTPException, status
from .session import create_ticket
from services.cloud import cloud
from fastapi.responses import JSONResponse
from settings.decorators import role_required

ticket = APIRouter()


@ticket.post("/ticket/create")
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


@ticket.get("/applicants")
async def get_all_applicants():
    try:
        applicants = collection.find()
        applicants_list = list(applicants)
        for applicant in applicants_list:
            applicant["_id"] = str(applicant["_id"])
        return {"applicants": applicants_list}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch applicants: {str(e)}"
        )
