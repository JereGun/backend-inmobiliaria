from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate # Added UsuarioUpdate
from app.crud.usuario_crud import usuario as crud_usuario
from tests.utils.utils import random_email, random_lower_string

API_V1_STR = "/api/v1" # Define this if not imported from settings

def test_login_access_token(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UsuarioCreate(email=email, password=password, is_active=True)
    crud_usuario.create_user(db, obj_in=user_in)

    login_data = {"username": email, "password": password}
    r = client.post(f"{API_V1_STR}/login/access-token", data=login_data)
    response_json = r.json()
    assert r.status_code == 200
    assert "access_token" in response_json
    assert response_json["token_type"] == "bearer"

def test_login_inactive_user(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UsuarioCreate(email=email, password=password, is_active=False) # Inactive user
    crud_usuario.create_user(db, obj_in=user_in)

    login_data = {"username": email, "password": password}
    r = client.post(f"{API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 400
    assert r.json()["detail"] == "Inactive user"

def test_login_wrong_password(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UsuarioCreate(email=email, password=password, is_active=True)
    crud_usuario.create_user(db, obj_in=user_in)

    login_data = {"username": email, "password": "wrong_password"}
    r = client.post(f"{API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 401

def test_get_users_me_ok(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in_db = crud_usuario.create_user(db, obj_in=UsuarioCreate(email=email, password=password, is_active=True))

    login_data = {"username": email, "password": password}
    r_login = client.post(f"{API_V1_STR}/login/access-token", data=login_data)
    token = r_login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    r_me = client.get(f"{API_V1_STR}/users/me", headers=headers)
    current_user = r_me.json()

    assert r_me.status_code == 200
    assert current_user["email"] == email
    assert current_user["id"] == user_in_db.id
    assert current_user["is_active"] is True # User.is_active from schema

def test_get_users_me_inactive_user_token(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    # User is created as active, logs in, then becomes inactive
    user_in_db = crud_usuario.create_user(db, obj_in=UsuarioCreate(email=email, password=password, is_active=True))

    login_data = {"username": email, "password": password}
    r_login = client.post(f"{API_V1_STR}/login/access-token", data=login_data)
    token = r_login.json()["access_token"]

    # Make user inactive AFTER token is generated
    crud_usuario.update_user(db, db_obj=user_in_db, obj_in=UsuarioUpdate(is_active=False))

    headers = {"Authorization": f"Bearer {token}"}
    r_me = client.get(f"{API_V1_STR}/users/me", headers=headers)
    assert r_me.status_code == 400 # get_current_active_user should raise this

def test_get_users_me_invalid_token(client: TestClient) -> None: # Removed db: Session as it's not directly used
    headers = {"Authorization": "Bearer invalidtoken"}
    r_me = client.get(f"{API_V1_STR}/users/me", headers=headers)
    assert r_me.status_code == 401
