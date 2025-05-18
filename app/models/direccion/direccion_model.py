from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Pais(Base):
    __tablename__ = "paises"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    #Relaciones
    provincias = relationship("Provincia", back_populates="pais")
    direcciones = relationship("Direccion", back_populates="pais")

class Provincia(Base):
    __tablename__ = "provincias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    #Relaciones
    pais_id = Column(Integer, ForeignKey("paises.id"))
    pais = relationship("Pais", back_populates="provincias")
    localidades = relationship("Localidad", back_populates="provincia")
    direcciones = relationship("Direccion", back_populates="provincia")

class Localidad(Base):
    __tablename__ = "localidades"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    #Relaciones
    provincia_id = Column(Integer, ForeignKey("provincias.id"))
    provincia = relationship("Provincia", back_populates="localidades")
    direcciones = relationship("Direccion", back_populates="localidad")

class Direccion(Base):
    __tablename__ = "direcciones"

    id = Column(Integer, primary_key=True, index=True)
    calle = Column(String, nullable=True)
    altura = Column(Integer, nullable=True)
    piso = Column(String, nullable=True)
    dpto = Column(String, nullable=True)
    entre_calles = Column(String, nullable=True)
    observaciones = Column(String, nullable=True)
    codigo_postal = Column(Integer, index=True)
    barrio = Column(String, index=True, nullable=True)
    #Relaciones
    localidad_id = Column(Integer, ForeignKey("localidades.id"))
    localidad = relationship("Localidad", back_populates="direcciones")
    provincia_id = Column(Integer, ForeignKey("provincias.id"))
    provincia = relationship("Provincia", back_populates="direcciones")
    pais_id = Column(Integer, ForeignKey("paises.id"))
    pais = relationship("Pais", back_populates="direcciones")
