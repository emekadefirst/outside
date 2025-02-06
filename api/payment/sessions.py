import uuid
from typing import List
from sqlmodel import select, Session
from .database import Payment, engine
from sqlalchemy.exc import SQLAlchemyError


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
            session.refresh(payment)  
            return payment
        except SQLAlchemyError as e:
            session.rollback()  # Ensure rollback in case of error
            raise Exception(f"Error creating payment: {e}")


def get_payment_by_id(payment_id: uuid.UUID) -> Payment:
    with Session(engine) as session:  # Use the synchronous session context
        try:
            result = session.execute(
                select(Payment).where(Payment.id == payment_id)
            )  # Execute query
            return result.scalar_one_or_none()  # Return a single result or None
        except SQLAlchemyError as e:
            raise Exception(f"Error retrieving payment by id: {e}")


def get_payments(skip: int = 0, limit: int = 100) -> List[Payment]:
    with Session(engine) as session:  # Use the synchronous session context
        try:
            result = session.execute(
                select(Payment).offset(skip).limit(limit)
            )  # Execute query with offset and limit
            return result.scalars().all()  # Return a list of payments
        except SQLAlchemyError as e:
            raise Exception(f"Error retrieving payments: {e}")
