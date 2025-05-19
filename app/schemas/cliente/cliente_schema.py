from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date, datetime
from app.models.enums import TipoDocumentoEnum, GeneroEnum, SituacionFiscalEnum


# TODO Cliente-Schema
class ClienteBase(BaseModel):
    nombre: str = Field(..., title="Nombre del cliente", description="Nombre o nombres del cliente")
    apellido: str = Field(..., title="Apellido del cliente", description="Apellido o apellidos del cliente")
    tipo_documento: TipoDocumentoEnum = Field(..., title="Tipo de documento", description="Tipo de documento del cliente")
    numero_documento: str = Field(..., title="Número de documento", description="Número de documento del cliente")
    email: Optional[EmailStr] = Field(None, title="Email del cliente", description="Email del cliente")
    telefono: Optional[str] = Field(None, title="Teléfono del cliente", description="Teléfono del cliente")
    celular: Optional[str] = Field(None, title="Celular del cliente", description="Celular del cliente")
    fecha_nacimiento: Optional[date] = Field(None, title="Fecha de nacimiento", description="Fecha de nacimiento del cliente")
    genero: Optional[GeneroEnum] = Field(None, title="Género del cliente", description="Género del cliente")
    situacion_fiscal: Optional[SituacionFiscalEnum] = Field(None, title="Situación fiscal del cliente", description="Situación fiscal del cliente")
    direccion_id: Optional[int] = Field(None, title="ID de la dirección", description="ID de la dirección del cliente")

class ClienteCreate(ClienteBase):
    """Esquema para crear un nuevo cliente"""
    pass

class ClienteOut(ClienteBase):
    id: int = Field(..., title="ID del cliente", description="Identificador único del cliente")
    fecha_alta: datetime = Field(..., title="Fecha de alta", description="Fecha de alta del cliente")

    model_config = {
        "from_attributes": True
    }
