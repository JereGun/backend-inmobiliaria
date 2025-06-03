from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from app.models.enums import EstadoContratoEnum # Import the enum
# Import schemas for related models if they are to be nested in the response
# from app.schemas.propiedad import Propiedad  # Assuming Propiedad schema for reading
# from app.schemas.cliente import Cliente    # Assuming Cliente schema for reading

class ContratoAlquilerBase(BaseModel):
    propiedad_id: int
    inquilino_id: int
    fecha_inicio: date
    fecha_fin: date
    monto_alquiler_inicial: int
    monto_alquiler_actual: int
    dia_pago_mensual: int
    intervalo_aumento_meses: int
    fecha_proximo_aumento: Optional[date] = None # Made Optional
    estado: EstadoContratoEnum

class ContratoAlquilerCreate(ContratoAlquilerBase):
    pass

class ContratoAlquilerUpdate(BaseModel):
    # All fields are optional for update
    propiedad_id: Optional[int] = None
    inquilino_id: Optional[int] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    monto_alquiler_inicial: Optional[int] = None # Usually not changed after creation
    monto_alquiler_actual: Optional[int] = None
    dia_pago_mensual: Optional[int] = None
    intervalo_aumento_meses: Optional[int] = None
    fecha_proximo_aumento: Optional[date] = None
    fecha_ultima_notificacion_aumento: Optional[datetime] = None
    estado: Optional[EstadoContratoEnum] = None

class ContratoAlquiler(ContratoAlquilerBase):
    id: int
    fecha_ultima_notificacion_aumento: Optional[datetime] = None
    # Add related models if they should be included when reading a contract
    # propiedad: Optional[Propiedad] = None # Example
    # inquilino: Optional[Cliente] = None # Example

    class Config:
        orm_mode = True
