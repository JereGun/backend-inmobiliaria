import pytest
from sqlalchemy.orm import Session
from app.crud.usuario_crud import usuario as crud_usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import verify_password # Ensure this path is correct
from tests.utils.utils import random_email, random_lower_string # Corrected import path

def test_create_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UsuarioCreate(email=email, password=password, is_active=True, is_superuser=False)
    user = crud_usuario.create_user(db, obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")
    assert verify_password(password, user.hashed_password)
    assert user.is_active is True
    assert user.is_superuser is False

def test_get_user_by_email(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UsuarioCreate(email=email, password=password)
    user = crud_usuario.create_user(db, obj_in=user_in)

    fetched_user = crud_usuario.get_user_by_email(db, email=email)
    assert fetched_user
    assert fetched_user.email == email
    assert fetched_user.id == user.id

def test_update_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UsuarioCreate(email=email, password=password)
    user = crud_usuario.create_user(db, obj_in=user_in)

    new_password = random_lower_string()
    user_update_data = UsuarioUpdate(password=new_password, is_active=False)
    updated_user = crud_usuario.update_user(db, db_obj=user, obj_in=user_update_data)

    assert updated_user.email == email
    assert verify_password(new_password, updated_user.hashed_password)
    assert updated_user.is_active is False
