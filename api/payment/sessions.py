import uuid
from typing import List
from sqlmodel import select, Session
from .database import Payment, engine


# CRUD Operations (Synchronous)
def create_payment(user, ticket_name, amount, reference_id, host):
    with Session(engine) as session:  
        try:
            payment = Payment(
                user=user,
                ticket_name=ticket_name,
                amount=amount,
                reference_id=reference_id,
                host=host,
            )
            session.add(payment)
            session.commit()  
            return payment
        except Exception as e:
            raise f"Error creating payment: {e}"


def get_payment_by_id(payment_id: uuid.UUID):
    with Session(engine) as session:  
        try:
            result = session.execute(select(Payment).where(Payment.id == payment_id))  
            return result.scalar_one_or_none() 
        except Exception as e:
            raise f"Error retrieving payment by id: {e}"


def get_payments(skip: int = 0, limit: int = 100) -> List[Payment]:
    with Session(engine) as session:  
        try:
            result = session.execute(select(Payment).offset(skip).limit(limit))  
            return result.scalars().all()  
        except Exception as e:
            raise f"Error retrieving payments: {e}"
