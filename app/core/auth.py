from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db # Assuming get_db is here
from app.core.security import ALGORITHM, JWT_SECRET_KEY
from app.schemas.token import TokenPayload
from app.models.usuario import Usuario
from app.crud.usuario_crud import usuario as crud_user # Ensure crud_user is correctly named and imported

# Adjust tokenUrl if your router is prefixed, e.g. /api/v1/login/access-token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/access-token")

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        # token_data = TokenPayload(sub=user_id) # Corrected: directly use user_id
    except JWTError:
        raise credentials_exception

    user = crud_user.get_user(db, user_id=int(user_id)) # Use user_id from payload
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: Usuario = Depends(get_current_user),
) -> Usuario:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_active_superuser(
    current_user: Usuario = Depends(get_current_active_user),
) -> Usuario:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
