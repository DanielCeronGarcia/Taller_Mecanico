from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, require_roles
from app.core.security import create_access_token, hash_password, verify_password
from app.db import get_db
from app.models import AuditLog, Customer, Role, User
from app.schemas.schemas import AccountRegister, AuditOut, CustomerCreate, CustomerOut, LoginInput, TokenResponse, UserCreate, UserOut, UserRoleUpdate
from app.services.customer_service import create_customer

router = APIRouter(prefix="/api/v1")


@router.post("/auth/login", response_model=TokenResponse)
def login(data: LoginInput, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == str(data.email).lower()))
    if not user or not user.is_active or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos.")
    return TokenResponse(access_token=create_access_token(user.email, user.role.value))


@router.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_account(data: AccountRegister, db: Session = Depends(get_db)):
    email = str(data.email).lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un usuario con ese correo.")
    user = User(email=email, full_name=data.full_name, password_hash=hash_password(data.password), role=Role.ADMINISTRADOR)
    try:
        db.add(user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un usuario con ese correo.")
    db.refresh(user)
    return user


@router.get("/auth/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(data: UserCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(Role.ADMINISTRADOR))):
    email = str(data.email).lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un usuario con ese correo.")
    user = User(email=email, full_name=data.full_name, password_hash=hash_password(data.password), role=data.role)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un usuario con ese correo.")
    db.refresh(user)
    return user


@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_roles(Role.ADMINISTRADOR))):
    return list(db.scalars(select(User).order_by(User.full_name)))


@router.patch("/users/{user_id}/role", response_model=UserOut)
def change_user_role(user_id: int, data: UserRoleUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_roles(Role.ADMINISTRADOR))):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
    if user.id == current_user.id and data.role != Role.ADMINISTRADOR:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No puede cambiar su propio rol de Administrador.")
    user.role = data.role
    db.commit()
    db.refresh(user)
    return user


@router.post("/customers", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
def register_customer(data: CustomerCreate, db: Session = Depends(get_db), user: User = Depends(require_roles(Role.ADMINISTRADOR, Role.RECEPCIONISTA))):
    return create_customer(db, data, user)


@router.get("/customers", response_model=list[CustomerOut])
def list_customers(db: Session = Depends(get_db), _: User = Depends(require_roles(Role.ADMINISTRADOR, Role.RECEPCIONISTA, Role.ASESOR))):
    return list(db.scalars(select(Customer).order_by(Customer.created_at.desc())))


@router.get("/consultas", response_model=list[AuditOut])
def list_queries(actor_role: Role | None = None, path: str | None = None, from_date: datetime | None = None, to_date: datetime | None = None, db: Session = Depends(get_db), _: User = Depends(require_roles(Role.ADMINISTRADOR))):
    query = select(AuditLog).order_by(AuditLog.created_at.desc())
    if actor_role:
        query = query.where(AuditLog.actor_role == actor_role.value)
    if path:
        query = query.where(AuditLog.path.contains(path))
    if from_date:
        query = query.where(AuditLog.created_at >= from_date)
    if to_date:
        query = query.where(AuditLog.created_at <= to_date)
    return list(db.scalars(query))
