from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Pais(Base):
    __tablename__ = "paises"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    
    provincias = relationship("Provincia", back_populates="pais")

class Provincia(Base):
    __tablename__ = "provincias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    pais_id = Column(Integer, ForeignKey("paises.id"))
    pais = relationship("Pais", back_populates="provincias")
    
    localidades = relationship("Localidad", back_populates="provincia")

class Localidad(Base):
    __tablename__ = "localidades"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    provincia_id = Column(Integer, ForeignKey("provincias.id"))
    provincia = relationship("Provincia", back_populates="localidades")

class Addres(Base):
    __tablename__ = "direcciones"

    id = Column(Integer, primary_key=True, index=True)
    calle = Column(String)
    altura = Column(Integer)
    codigo_postal = Column(Integer, index=True)
    barrio = Column(String, index=True)
    localidad_id = Column(Integer, ForeignKey("localidades.id"))
    localidad = relationship("Localidad", back_populates="direcciones")
    provincia_id = Column(Integer, ForeignKey("provincias.id"))
    provincia = relationship("Provincia", back_populates="direcciones")
    pais_id = Column(Integer, ForeignKey("paises.id"))
    pais = relationship("Pais", back_populates="direcciones")
