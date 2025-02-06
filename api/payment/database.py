import os
import uuid
import random
import string
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv
from sqlmodel import SQLModel, Field, create_engine


load_dotenv()


DATABASE_URL = os.getenv("POSTGRESQL")
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def generate_ticket_code(length=8, used_codes=set()):
    """Generates a random, unique ticket code."""
    while True:
        ticket_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=length)
        )
        if ticket_code not in used_codes:
            used_codes.add(ticket_code)
            return ticket_code

class Payment(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(primary_key=True, default_factory=uuid.uuid4)
    user: str = Field(unique=True, max_length=150)
    ticket_name: str = Field()
    amount: str
    host: str
    reference_id: str = Field(unique=True)
    ticket_code: Optional[str] = Field(unique=True)
    status: str = Field(default="processing")
    payment_service: str = Field(default="Paystack")
    created_at: datetime = Field(default_factory=datetime.now)

    def save(self, *args, **kwargs):
        if self.status == "success":
            self.ticket_code = generate_ticket_code()

    def __str__(self):
        return self.user
    
create_db_and_tables()