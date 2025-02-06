from pydantic import BaseModel

class Payment(BaseModel):
    ticket_id: str
    user_id: str


class UpdatePaymentStatus(BaseModel):
    status: str 

