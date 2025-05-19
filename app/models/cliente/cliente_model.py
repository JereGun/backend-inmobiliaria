from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime

class TipoDocumentoEnum(str, enum.Enum):
    DNI = "DNI"
    CUIT = "CUIT"
    CUIL = "CUIL"
    PASAPORTE = "PASAPORTE"
    OTRO = "OTRO"

class GeneroEnum(str, enum.Enum):
    MASCULINO = "MASCULINO"
    FEMENINO = "FEMENINO"
    OTRO = "OTRO"

class SituacionFiscalEnum(str, enum.Enum):
    RESPONSABLE_INSCRIPTO = "RESPONSABLE_INSCRIPTO"
    RESPONSABLE_NO_INSCRIPTO = "RESPONSABLE_NO_INSCRIPTO"
    EXENTO = "EXENTO"
    CONSUMIDOR_FINAL = "CONSUMIDOR_FINAL"
    MONOTRIBUTO = "MONOTRIBUTO"
    NO_RESPONSABLE = "NO_RESPONSABLE"
    OTRO = "OTRO"

class Cliente (Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    tipo_documento = Column(SQLAlchemyEnum(TipoDocumentoEnum, name="tipo_documento_enum"), nullable=False, default=TipoDocumentoEnum.DNI)
    numero_documento = Column(String, unique=True, index=True)
    email = Column(String(255), unique=True)
    telefono = Column(String, nullable=True)
    celular = Column(String, nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    fecha_alta = Column(DateTime, default=datetime.utcnow)
    genero = Column(SQLAlchemyEnum(GeneroEnum, name="genero_enum"), nullable=True)
    situacion_fiscal = Column(SQLAlchemyEnum(SituacionFiscalEnum, name="situacion_fiscal_enum"), nullable=True)
    
    #Relaciones
    direccion_id = Column(Integer, ForeignKey("direcciones.id"), nullable=True)
    direccion = relationship("Direccion", back_populates="clientes")