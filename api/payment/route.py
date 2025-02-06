import uuid
from fastapi import APIRouter, HTTPException
from .schema import Payment
from user.backend import get_user  
from ticket.session import get_ticket  
from services.paystack import initialize_transaction
from .sessions import create_payment, get_payments, get_payment_by_id

payment = APIRouter()

@payment.post("/payments/create")
async def create_payment_endpoint(data: Payment):
    try:
        user = get_user(data.user_id) 
        ticket = get_ticket(data.ticket_id)  

        if user and ticket:
            email = user["data"]["email"]
            amount = ticket["ticket"]["unit_price"]
            response = await initialize_transaction(
                email, amount
            )  
            create_payment(
                user=user["data"]["username"],
                amount=amount,
                host=ticket["ticket"]["user_id"],
                reference_id=response["reference"],
                ticket_name=ticket["ticket"]["name"],
            )

            return {"authorization_url": response["authorization_url"]}
        raise HTTPException(status_code=400, detail="User or Ticket not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@payment.get("/payments")
async def get_all_payment():
    return get_payments()


@payment.get("/payments/{id}")
async def payment_by_id(id: uuid.UUID):
    return get_payment_by_id(id)
