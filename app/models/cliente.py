from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
from app.models.enums import tipo_documento_enum, genero_enum, situacion_fiscal_enum

class Cliente (Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    tipo_documento = Column(tipo_documento_enum, nullable=False, default="DNI")
    numero_documento = Column(String, unique=True, index=True)
    email = Column(String(255), unique=True)
    telefono = Column(String, nullable=True)
    celular = Column(String, nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    fecha_alta = Column(DateTime, default=datetime.utcnow)
    genero = Column(genero_enum, nullable=True)
    situacion_fiscal = Column(situacion_fiscal_enum, nullable=True)
    
    #Relaciones
    direccion_id = Column(Integer, ForeignKey("direcciones.id"), nullable=True)
    direccion = relationship("Direccion", back_populates="clientes")
    propiedades = relationship("Propiedad", back_populates="propietario")