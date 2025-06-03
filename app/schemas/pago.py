from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from decimal import Decimal
from app.models.enums import MetodoPagoEnum
# from .factura import FacturaBase # If nesting Factura in Pago response

class PagoBase(BaseModel):
    factura_id: int
    fecha_pago: date
    monto_pagado: Decimal = Field(..., gt=0, decimal_places=2) # Must be greater than 0
    metodo_pago: MetodoPagoEnum
    referencia_pago: Optional[str] = None

    class Config:
        use_enum_values = True

class PagoCreate(PagoBase):
    pass

class PagoUpdate(BaseModel): # Pagos are usually not updated, but some fields might be corrected
    fecha_pago: Optional[date] = None
    monto_pagado: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    metodo_pago: Optional[MetodoPagoEnum] = None
    referencia_pago: Optional[str] = None

    class Config:
        use_enum_values = True

class Pago(PagoBase): # Schema for reading (response model)
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    # factura: Optional[FacturaBase] = None # Example if you want to nest factura info

    class Config:
        orm_mode = True
        use_enum_values = True
