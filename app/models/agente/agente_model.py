from app.database import Base
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, DateTime
from app.models.enums import tipo_documento_enum
from sqlalchemy.orm import relationship
from datetime import datetime

class Agente(Base):
    __tablename__ = "agentes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    tipo_documento = Column(tipo_documento_enum, nullable=False, default="DNI")
    numero_documento = Column(String, unique=True, index=True)
    telefono = Column(String, nullable=False)
    email = Column(String(255), nullable=False)
    fecha_nacimiento = Column(DateTime, nullable=False)
    activo = Column(Boolean, default=True)
    direccion_id = Column(Integer, ForeignKey("direcciones.id"), nullable=True)  # Direccion FK
    licencia = Column(String, nullable=False)
    fecha_alta = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, nullable=True)
    # Relacion con Direccion
    direccion = relationship("Direccion", back_populates="agentes")
