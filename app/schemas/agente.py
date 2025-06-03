from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date, datetime
from app.models.enums import TipoDocumentoEnum
from app.schemas.direccion import DireccionCreateNested


class AgenteBase(BaseModel):
    nombre: str = Field(..., title="Nombre del agente", description="Nombre o nombres del agente")
    apellido: str = Field(..., title="Apellido del agente", description="Apellido o apellidos del agente")
    tipo_documento: TipoDocumentoEnum = Field(..., title="Tipo de documento", description="Tipo de documento del agente")
    numero_documento: str = Field(..., title="Número de documento", description="Número de documento del agente")
    telefono: Optional[str] = Field(..., title="Teléfono del agente", description="Teléfono del agente")
    email: Optional[EmailStr] = Field(..., title="Email del agente", description="Email del agente")
    fecha_nacimiento: Optional[date] = Field(..., title="Fecha de nacimiento", description="Fecha de nacimiento del agente")
    licencia: str = Field(..., title="Número de licencia", description="Número de licencia del agente")
    direccion_id: Optional[int] = Field(None, title="ID de la dirección", description="ID de la dirección del agente")
    activo: Optional[bool] = Field(True, title="Estado del agente", description="Estado del agente")

class AgenteCreate(AgenteBase):
    """Esquema para crear un nuevo agente"""
    direccion: Optional[DireccionCreateNested] = Field(None, title="Dirección del agente", description="Dirección del agente para crear")

class AgenteOut(AgenteBase):
    id: int = Field(..., title="ID del agente", description="Identificador único del agente")
    fecha_alta: datetime = Field(..., title="Fecha de alta", description="Fecha de alta del agente")

    model_config = {
        "from_attributes": True
    }

