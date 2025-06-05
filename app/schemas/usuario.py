from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

class UsuarioInDBBase(UsuarioBase):
    id: int

    class Config:
        orm_mode = True

# For responses, typically includes all fields except password
class Usuario(UsuarioInDBBase):
    pass

class UsuarioInDB(UsuarioInDBBase):
    hashed_password: str
