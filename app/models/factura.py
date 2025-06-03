from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Text, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime # For default dates
from app.models.enums import tipo_factura_enum, estado_pago_factura_enum, EstadoPagoFacturaEnum

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    contrato_alquiler_id = Column(Integer, ForeignKey("contratos_alquiler.id"), nullable=True)
    propiedad_id = Column(Integer, ForeignKey("propiedades.id"), nullable=True) # For sales or property-specific services

    tipo_factura = Column(tipo_factura_enum, nullable=False)
    serie_factura = Column(String(10), nullable=True) # E.g., "0001"
    numero_factura = Column(Integer, nullable=True) # E.g., 1, 2, 3... (could be unique per serie)

    fecha_emision = Column(Date, nullable=False, default=datetime.utcnow)
    fecha_vencimiento = Column(Date, nullable=True)

    monto_base = Column(Numeric(10, 2), nullable=False, default=0.0) # Amount before IVA
    monto_iva = Column(Numeric(10, 2), nullable=False, default=0.0)   # IVA amount
    monto_total = Column(Numeric(10, 2), nullable=False, default=0.0) # Base + IVA
    monto_adeudado = Column(Numeric(10, 2), nullable=False, default=0.0) # Amount pending payment

    estado_pago = Column(estado_pago_factura_enum, nullable=False, default=EstadoPagoFacturaEnum.PENDIENTE)
    descripcion_items = Column(Text, nullable=True) # Simple description for now, or JSON for multiple items

    # Timestamps
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    cliente = relationship("Cliente") # Assuming Cliente model has a back_populates="facturas"
    contrato_alquiler = relationship("ContratoAlquiler") # Assuming ContratoAlquiler model has back_populates="facturas"
    propiedad = relationship("Propiedad") # Assuming Propiedad model has back_populates="facturas"
    pagos = relationship("Pago", back_populates="factura", cascade="all, delete-orphan")

    # Consider adding a unique constraint for (serie_factura, numero_factura) if they should be unique together
    # from sqlalchemy import UniqueConstraint
    # __table_args__ = (UniqueConstraint('serie_factura', 'numero_factura', name='_serie_numero_uc'),)
