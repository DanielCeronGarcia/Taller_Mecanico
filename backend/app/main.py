from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.config import get_settings
from app.core.security import hash_password
import jwt
from app.db import Base, SessionLocal, engine
from app.models import AuditLog, Role, User


def seed_admin() -> None:
    settings = get_settings()
    with SessionLocal() as db:
        exists = db.query(User).filter(User.email == settings.first_admin_email.lower()).first()
        if not exists:
            db.add(User(email=settings.first_admin_email.lower(), full_name="Administrador inicial", password_hash=hash_password(settings.first_admin_password), role=Role.ADMINISTRADOR))
            db.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_admin()
    yield


app = FastAPI(title="API Taller Mecánico", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=get_settings().origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)


@app.middleware("http")
async def audit_requests(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/api/"):
        # AUTOMATICO describe el origen de una auditoría sin usuario; no es un rol asignable.
        actor_email, actor_role = None, "AUTOMATICO"
        token = request.headers.get("authorization", "").removeprefix("Bearer ")
        if token:
            try:
                claims = jwt.decode(token, get_settings().jwt_secret, algorithms=[get_settings().jwt_algorithm])
                actor_email, actor_role = claims.get("sub"), claims.get("role")
            except jwt.PyJWTError:
                pass
        with SessionLocal() as db:
            db.add(AuditLog(actor_email=actor_email, actor_role=actor_role, method=request.method, path=request.url.path, status_code=response.status_code))
            db.commit()
    return response


@app.get("/health")
def health():
    return {"status": "ok"}
