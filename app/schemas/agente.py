from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.enums import TipoDocumentoEnum # Changed to import the Python Enum
from app.schemas.usuario import UsuarioBase, UsuarioCreate # Import new User schemas

# AgenteBase will now define fields specific to Agente,
# email and user status fields will come from Usuario parts.
class AgenteBase(BaseModel):
    nombre: str
    apellido: str
    tipo_documento: Optional[TipoDocumentoEnum] = TipoDocumentoEnum.DNI # Use Python Enum
    numero_documento: str
    telefono: str
    # email is removed, will be part of user creation
    fecha_nacimiento: datetime
    activo: Optional[bool] = True # This is Agente.activo, distinct from Usuario.is_active
    direccion_id: Optional[int] = None
    licencia: str

# For creating an Agente, we need both User info and Agente info.
# We can compose this by including all fields.
class AgenteCreate(AgenteBase):
    email: EmailStr # From Usuario
    password: str   # From Usuario

class AgenteUpdate(BaseModel):
    # Agente specific fields
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    tipo_documento: Optional[TipoDocumentoEnum] = None # Use Python Enum
    numero_documento: Optional[str] = None
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    activo: Optional[bool] = None # Agente.activo
    direccion_id: Optional[int] = None
    licencia: Optional[str] = None
    # User specific fields (optional for update)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None # Usuario.is_active

# Schema for reading Agente data, including inherited User fields
class Agente(AgenteBase): # Inherits Agente-specific fields
    id: int                 # Agente's ID (which is also User's ID)
    email: EmailStr         # From User
    is_active: bool         # From User (Usuario.is_active)
    is_superuser: bool      # From User
    fecha_alta: datetime
    fecha_modificacion: Optional[datetime] = None

    class Config:
        orm_mode = True

# If you need a separate AgenteInDB that might include more, like hashed_password from User
# for internal use, you could define it. But for API responses, 'Agente' schema is typical.
class AgenteInDB(Agente): # For now, same as Agente response
    pass
