import pytest
from pydantic import ValidationError
from app.schemas.schemas import CustomerCreate, UserCreate


def test_customer_schema_normalizes_name():
    customer = CustomerCreate(name="  Ana   Torres ", email="ana@example.com", phone="5512345678")
    assert customer.name == "Ana Torres"


@pytest.mark.parametrize("phone", ["5512", "teléfono", "5512345678901234"])
def test_customer_schema_rejects_invalid_phone(phone):
    with pytest.raises(ValidationError):
        CustomerCreate(name="Ana Torres", email="ana@example.com", phone=phone)


def test_only_defined_roles_are_accepted():
    with pytest.raises(ValidationError):
        UserCreate(full_name="Rol inválido", email="invalid@example.com", password="ClaveSegura123", role="SISTEMA")
