from pydantic import BaseModel



class Payment(BaseModel):
    ticket_id: str
    user_id: str