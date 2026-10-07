from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models import Customer, User
from app.schemas.schemas import CustomerCreate


def create_customer(db: Session, data: CustomerCreate, creator: User) -> Customer:
    duplicate = db.scalar(select(Customer).where(or_(Customer.email == str(data.email), Customer.phone == data.phone)))
    if duplicate:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un cliente con ese correo o teléfono.")
    customer = Customer(name=data.name, email=str(data.email).lower(), phone=data.phone, created_by_id=creator.id)
    db.add(customer)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un cliente con ese correo o teléfono.")
    db.refresh(customer)
    return customer
