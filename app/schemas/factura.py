from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal # For monetary values
from app.models.enums import TipoFacturaEnum, EstadoPagoFacturaEnum
# Forward declaration for Pago schema to avoid circular import if Pago schema includes Factura
# from .pago import Pago # This will be defined in pago.py; only needed if nesting full objects

class FacturaBase(BaseModel):
    cliente_id: int
    contrato_alquiler_id: Optional[int] = None
    propiedad_id: Optional[int] = None
    tipo_factura: TipoFacturaEnum
    serie_factura: Optional[str] = Field(None, max_length=10)
    numero_factura: Optional[int] = None
    fecha_emision: date
    fecha_vencimiento: Optional[date] = None
    monto_base: Decimal = Field(..., ge=0, decimal_places=2)
    monto_iva: Decimal = Field(..., ge=0, decimal_places=2)
    monto_total: Decimal = Field(..., ge=0, decimal_places=2) # Will often be calculated
    estado_pago: EstadoPagoFacturaEnum = EstadoPagoFacturaEnum.PENDIENTE
    descripcion_items: Optional[str] = None

    class Config:
        use_enum_values = True # Ensure enum values are used, not enum objects

class FacturaCreate(FacturaBase):
    # monto_adeudado will be set automatically to monto_total on creation in CRUD
    pass

class FacturaUpdate(BaseModel):
    cliente_id: Optional[int] = None
    contrato_alquiler_id: Optional[int] = None
    propiedad_id: Optional[int] = None
    tipo_factura: Optional[TipoFacturaEnum] = None
    serie_factura: Optional[str] = Field(None, max_length=10)
    numero_factura: Optional[int] = None
    fecha_emision: Optional[date] = None
    fecha_vencimiento: Optional[date] = None
    monto_base: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    monto_iva: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    monto_total: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    # estado_pago and monto_adeudado are typically updated by payment logic, not direct update
    # But allow admin override for estado_pago (e.g., ANULADA)
    estado_pago: Optional[EstadoPagoFacturaEnum] = None
    descripcion_items: Optional[str] = None

    class Config:
        use_enum_values = True

# Forward declaration for Pago in Factura schema
class Pago(BaseModel): # Basic structure for Pago to be nested in Factura
    id: int
    fecha_pago: date
    monto_pagado: Decimal
    metodo_pago: str # Assuming MetodoPagoEnum will be string here
    referencia_pago: Optional[str] = None
    class Config:
        orm_mode = True
        use_enum_values = True


class Factura(FacturaBase): # Schema for reading (response model)
    id: int
    monto_adeudado: Decimal = Field(..., ge=0, decimal_places=2)
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    pagos: List[Pago] = [] # List of payments

    class Config:
        orm_mode = True
        use_enum_values = True
