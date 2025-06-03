from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
from app.models.enums import estado_contrato_enum # Import the new enum

class ContratoAlquiler(Base):
    __tablename__ = "contratos_alquiler"

    id = Column(Integer, primary_key=True, index=True)
    propiedad_id = Column(Integer, ForeignKey("propiedades.id"), nullable=False)
    inquilino_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    monto_alquiler_inicial = Column(Integer, nullable=False)
    monto_alquiler_actual = Column(Integer, nullable=False)
    dia_pago_mensual = Column(Integer, nullable=False) # e.g., 1 to 10
    intervalo_aumento_meses = Column(Integer, nullable=False) # e.g., 3, 6, 12
    fecha_proximo_aumento = Column(Date, nullable=False)
    fecha_ultima_notificacion_aumento = Column(DateTime, nullable=True)
    estado = Column(estado_contrato_enum, nullable=False, default=estado_contrato_enum.enums[0]) # Default to VIGENTE

    # Relationships
    propiedad = relationship("Propiedad") # Define relationship to Propiedad
    inquilino = relationship("Cliente")  # Define relationship to Cliente

    # It might be useful to add back_populates if these relationships become bidirectional later
    # For example, if Propiedad needs to list its contracts or Cliente its rental history.
    # propiedad = relationship("Propiedad", back_populates="contratos")
    # inquilino = relationship("Cliente", back_populates="contratos_alquiler")
