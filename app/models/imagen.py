from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from app.core.database import Base

# Cambia la clase Base por la importada
class Imagen(Base):
    __tablename__ = "imagenes"
    
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    tipo_imagen = Column(String(50), nullable=False)
    
    __mapper_args__ = {
        "polymorphic_on": tipo_imagen,
        "polymorphic_identity": "imagen"
    }

class ImagenPropiedad(Imagen):
    __tablename__ = "imagenes_propiedad"

    id = Column(Integer, ForeignKey("imagenes.id"), primary_key=True)
    propiedad_id = Column(Integer, ForeignKey("propiedades.id"), nullable=False, index=True)
    
    propiedad = relationship("Propiedad", back_populates="imagenes", foreign_keys=[propiedad_id], lazy="joined")
    
    __mapper_args__ = {
        "polymorphic_identity": "propiedad",
    }

class ImagenAgente(Imagen):
    __tablename__ = "imagenes_agente"
    
    id = Column(Integer, ForeignKey("imagenes.id"), primary_key=True)
    agente_id = Column(Integer, ForeignKey("agentes.id"), nullable=False, index=True)
    
    agente = relationship("Agente", back_populates="imagenes", lazy="joined")
    
    __mapper_args__ = {
        "polymorphic_identity": "agente",
    }