import uuid
import traceback
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

        if not user or "data" not in user or "email" not in user["data"]:
            raise HTTPException(status_code=400, detail="Invalid user data.")

        if not ticket or "ticket" not in ticket or "unit_price" not in ticket["ticket"]:
            raise HTTPException(status_code=400, detail="Invalid ticket data.")

        email = user["data"]["email"]
        amount = ticket["ticket"]["unit_price"]

        response = await initialize_transaction(email, amount)
        if not response or "authorization_url" not in response or "reference" not in response:
            raise HTTPException(status_code=500, detail="Payment initialization failed.")

        create_payment(
            user=user["data"]["username"],
            amount=amount,
            host=ticket["ticket"]["user_id"],
            reference_id=response["reference"],
            ticket_name=ticket["ticket"]["name"],
        )

        return {"authorization_url": response["authorization_url"]}
    
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}\n{traceback.format_exc()}"
        print(error_message)  # Logs full error traceback
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again.")


@payment.get("/payments")
async def get_all_payment():
    return get_payments()


@payment.get("/payments/{id}")
async def payment_by_id(id: uuid.UUID):
    return get_payment_by_id(id)
