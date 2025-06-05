from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.enums import tipo_propiedad_enum, tipo_operacion_enum, estado_enum
from datetime import datetime

class Propiedad (Base):
    __tablename__ = "propiedades"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    portada_id = Column(Integer, ForeignKey("imagenes_propiedad.id"), nullable=True) # Imagen para Portada FK
    direccion_id = Column(Integer, ForeignKey("direcciones.id"), nullable=False) # Direccion FK
    tipo_propiedad = Column(tipo_propiedad_enum, nullable=False, default="Casa")
    tipo_operacion = Column(tipo_operacion_enum, nullable=False, default="Alquiler")
    precio_venta = Column(Integer, nullable=True)
    precio_alquiler = Column(Integer, nullable=True)
    propietario_id = Column(Integer, ForeignKey("clientes.id"), nullable=True) # Cliente FK
    estado = Column(estado_enum, nullable=False, default="BORRADOR")
    descripcion = Column(String, nullable=True)
    # Caracteristicas
    ano_construccion = Column(Integer, nullable=True)
    banios = Column(Integer, nullable=True)
    dormitorios = Column(Integer, nullable=True)
    ambientes = Column(Integer, nullable=True)
    cochera = Column(Integer, nullable=True)
    amoblado = Column(Boolean, nullable=True)
    superficie_cubierta = Column(Integer, nullable=True)
    superficie_descubierta = Column(Integer, nullable=True)
    superficie_total = Column(Integer, nullable=True) # Removed problematic default
    agente_id = Column(Integer, ForeignKey("agentes.id"), nullable=True) # Agente FK
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, nullable=True)
    portada_id = Column(Integer, ForeignKey("imagenes_propiedad.id", use_alter=True, name="fk_propiedad_portada"), nullable=True) # Imagen para Portada FK
    # Relaciones
    direccion = relationship("Direccion", back_populates="propiedades")
    propietario = relationship("Cliente", back_populates="propiedades")
    agente = relationship("Agente", back_populates="propiedades")
    imagenes = relationship(
        "ImagenPropiedad", 
        back_populates="propiedad",
        foreign_keys="[ImagenPropiedad.propiedad_id]",
        primaryjoin="Propiedad.id == ImagenPropiedad.propiedad_id"
    )
    portada = relationship(
        "ImagenPropiedad",
        uselist=False,
        foreign_keys="[Propiedad.portada_id]",
        primaryjoin="Propiedad.portada_id == ImagenPropiedad.id"
    )