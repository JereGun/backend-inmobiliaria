from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
from app.models.enums import metodo_pago_enum

class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)

    fecha_pago = Column(Date, nullable=False, default=datetime.utcnow)
    monto_pagado = Column(Numeric(10, 2), nullable=False)
    metodo_pago = Column(metodo_pago_enum, nullable=False)
    referencia_pago = Column(String, nullable=True) # E.g., transaction ID, check number

    # Timestamps
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to Factura
    factura = relationship("Factura", back_populates="pagos")
