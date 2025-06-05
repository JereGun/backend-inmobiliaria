import pytest
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.crud.agente_crud import agente as crud_agente
from app.crud.usuario_crud import usuario as crud_usuario
from app.schemas.agente import AgenteCreate, AgenteUpdate
from app.schemas.usuario import UsuarioUpdate # Added for test_update_agente
from app.models.enums import TipoDocumentoEnum # Corrected import
from tests.utils.utils import random_email, random_lower_string, random_string # Corrected path from previous subtask

def test_create_agente(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    nombre = random_string()
    apellido = random_string()
    # Ensure numero_documento is unique enough for tests, perhaps by appending a random part
    numero_documento = f"DOC{random_string(7)}"

    agente_in = AgenteCreate(
        email=email,
        password=password,
        nombre=nombre,
        apellido=apellido,
        tipo_documento=TipoDocumentoEnum.DNI, # Corrected usage
        numero_documento=numero_documento,
        telefono=random_string(10),
        fecha_nacimiento=datetime.utcnow() - timedelta(days=365 * 20), # 20 years old
        licencia=random_string(10),
        # activo is part of AgenteBase, defaults to True if not provided by AgenteCreate schema
    )
    agente = crud_agente.create(db, obj_in=agente_in)

    assert agente.nombre == nombre
    assert agente.apellido == apellido
    assert agente.numero_documento == numero_documento
    assert agente.id is not None

    user = crud_usuario.get_user_by_email(db, email=email)
    assert user
    assert user.id == agente.id
    assert user.is_active is True # Default from Usuario model

    # Verify Agente.activo (distinct from User.is_active)
    # Agente.activo default is True in the model. AgenteCreate schema might not set it.
    assert agente.activo is True


def test_get_agente(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    nombre = random_string()
    numero_documento = f"DOC{random_string(7)}"
    agente_in_create = AgenteCreate(
        email=email, password=password, nombre=nombre, apellido=random_string(),
        tipo_documento=TipoDocumentoEnum.DNI, numero_documento=numero_documento, # Corrected usage
        telefono=random_string(10), fecha_nacimiento=datetime.utcnow() - timedelta(days=365*20),
        licencia=random_string(10)
    )
    agente = crud_agente.create(db, obj_in=agente_in_create)

    fetched_agente = crud_agente.get(db, id=agente.id)
    assert fetched_agente
    assert fetched_agente.id == agente.id
    assert fetched_agente.nombre == nombre
    # Check inherited email; Agente schema for reading should include it
    db.refresh(fetched_agente) # Ensure all attributes are loaded
    # The 'email' attribute on the Agente model instance might not be directly populated by default
    # by SQLAlchemy joined table inheritance in the way Pydantic expects for schema validation
    # unless explicitly loaded or defined in the query.
    # The Pydantic schema 'Agente' should map 'email' from the related user.
    # Let's fetch the user to confirm email.
    user = crud_usuario.get_user(db, user_id=fetched_agente.id)
    assert user.email == email


def test_update_agente(db: Session) -> None:
    email_orig = random_email()
    password_orig = random_lower_string()
    nombre_orig = random_string()
    numero_documento = f"DOC{random_string(7)}"
    agente_in_create = AgenteCreate(
        email=email_orig, password=password_orig, nombre=nombre_orig, apellido="OriginalApellido",
        tipo_documento=TipoDocumentoEnum.DNI, numero_documento=numero_documento, # Corrected usage
        telefono="1234567890", fecha_nacimiento=datetime.utcnow() - timedelta(days=365*25),
        licencia="LIC123"
    )
    agente = crud_agente.create(db, obj_in=agente_in_create)

    nombre_new = "UpdatedNombre"
    email_new = random_email()

    # AgenteUpdate schema allows updating 'email' and 'is_active' for the User part,
    # and 'activo' for the Agente part.
    agente_update_data = AgenteUpdate(nombre=nombre_new, email=email_new, activo=False, is_active=False)

    updated_agente = crud_agente.update(db, db_obj=agente, obj_in=agente_update_data)
    db.refresh(updated_agente) # Refresh to get latest state

    assert updated_agente.nombre == nombre_new
    assert updated_agente.activo is False # Agente.activo

    user = crud_usuario.get_user(db, user_id=updated_agente.id)
    assert user.email == email_new
    assert user.is_active is False # User.is_active


def test_remove_agente(db: Session) -> None:
    email = random_email()
    numero_documento = f"DOC{random_string(7)}"
    agente_in_create = AgenteCreate(
        email=email, password=random_lower_string(), nombre=random_string(), apellido=random_string(),
        tipo_documento=TipoDocumentoEnum.DNI, numero_documento=numero_documento, # Corrected usage
        telefono=random_string(10), fecha_nacimiento=datetime.utcnow() - timedelta(days=365*20),
        licencia=random_string(10)
    )
    agente = crud_agente.create(db, obj_in=agente_in_create)
    agente_id = agente.id

    crud_agente.remove(db, id=agente_id)

    deleted_agente = crud_agente.get(db, id=agente_id)
    assert deleted_agente is None

    deleted_user = crud_usuario.get_user(db, user_id=agente_id)
    assert deleted_user is None
