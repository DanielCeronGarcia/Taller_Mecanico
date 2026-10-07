from app.core.security import hash_password
from app.db import SessionLocal
from app.models import Role, User


def auth(client, email="admin@taller.example.com", password="CambieEstaClave123!"):
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_private_endpoint_requires_login(client):
    assert client.get("/api/v1/customers").status_code == 401


def test_admin_can_register_customer_and_prevents_duplicate(client):
    headers = auth(client)
    payload = {"name": "María López", "email": "maria@example.com", "phone": "5512345678"}
    assert client.post("/api/v1/customers", json=payload, headers=headers).status_code == 201
    assert client.post("/api/v1/customers", json=payload, headers=headers).status_code == 409


def test_receptionist_can_register_but_technician_cannot(client):
    with SessionLocal() as db:
        db.add_all([
            User(email="recepcion@example.com", full_name="Recepción", password_hash=hash_password("ClaveSegura123"), role=Role.RECEPCIONISTA),
            User(email="tecnico@example.com", full_name="Técnico", password_hash=hash_password("ClaveSegura123"), role=Role.TECNICO),
        ])
        db.commit()
    payload = {"name": "Juan Pérez", "email": "juan@example.com", "phone": "5512345679"}
    assert client.post("/api/v1/customers", json=payload, headers=auth(client, "recepcion@example.com", "ClaveSegura123")).status_code == 201
    rejected = client.post("/api/v1/customers", json={**payload, "email": "otro@example.com", "phone": "5512345680"}, headers=auth(client, "tecnico@example.com", "ClaveSegura123"))
    assert rejected.status_code == 403


def test_admin_cannot_create_duplicate_user(client):
    headers = auth(client)
    payload = {"full_name": "Nuevo Asesor", "email": "asesor@example.com", "password": "ClaveSegura123", "role": "ASESOR"}
    assert client.post("/api/v1/users", json=payload, headers=headers).status_code == 201
    assert client.post("/api/v1/users", json=payload, headers=headers).status_code == 409


def test_admin_can_list_users_and_change_role(client):
    headers = auth(client)
    created = client.post("/api/v1/users", json={"full_name": "Asesor Uno", "email": "asesor1@example.com", "password": "ClaveSegura123", "role": "ASESOR"}, headers=headers)
    user_id = created.json()["id"]
    assert client.get("/api/v1/users", headers=headers).status_code == 200
    changed = client.patch(f"/api/v1/users/{user_id}/role", json={"role": "TECNICO"}, headers=headers)
    assert changed.status_code == 200
    assert changed.json()["role"] == "TECNICO"


def test_admin_cannot_remove_own_administrator_role(client):
    headers = auth(client)
    me = client.get("/api/v1/auth/me", headers=headers).json()
    response = client.patch(f"/api/v1/users/{me['id']}/role", json={"role": "RECEPCIONISTA"}, headers=headers)
    assert response.status_code == 400
