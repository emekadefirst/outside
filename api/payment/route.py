from .schema import Payment
from user.backend import get_user
from ticket.session import get_ticket
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from services.paystack import initialize_transaction


payment = APIRouter()


@payment.post("/payment/create")
async def create_payment_endpoint(data: Payment):
    try:
        user = get_user(data.user_id)
        ticket = get_ticket(data.ticket_id)
        if user and ticket:
            email = user["email"]
            amount = ticket["unit_price"]
            response = await initialize_transaction(email, amount)
        return response 
    except Exception as e:
        return {"error": str(e)}
