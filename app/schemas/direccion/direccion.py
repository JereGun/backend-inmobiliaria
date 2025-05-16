from pydantic import BaseModel, Field
from typing import Optional

# Pais
class PaisBase(BaseModel):
    nombre: str = Field(..., title="Nombre del pais", description="Nombre oficial del pais en español")

class PaisCreate(PaisBase):
    """Esquema para crear un nuevo pais"""
    pass

class PaisOut(PaisBase):
    id: int = Field(..., title="ID del pais", description="Identificador unico del pais")
    
    class Config:
        orm_mode = True
 
# Provincia
class ProvinciaBase(BaseModel):
    nombre: str = Field(..., title="Nombre de la provincia", description="Nombre oficial de la provincia.")
    pais_id: int = Field(..., title="ID del país", description="ID del país al que pertenece la provincia.")

class ProvinciaCreate(ProvinciaBase):
    """Esquema para crear una nueva provincia"""
    pass

class ProvinciaOut(ProvinciaBase):
    id: int = Field(..., title="ID de la provincia", description="Identificador unico de la provincia")
    nombre: str = Field(..., title="Nombre de la provincia", description="Nombre oficial de la provincia.")
    pais_id: int = Field(..., title="ID del país", description="ID del país al que pertenece la provincia.")
    pais: Optional[PaisOut] = None

    class Config:
        orm_mode = True

class LocalidadBase(BaseModel):
    nombre: str = Field(..., title="Nombre de la localidad", description="Nombre oficial de la localidad.")
    provincia_id: int = Field(..., title="ID de la provincia", description="ID de la provincia a la que pertenece la localidad.")

class LocalidadCreate(LocalidadBase):
    """Esquema para crear una nueva localidad"""
    pass

class LocalidadOut(LocalidadBase):
    id: int = Field(..., title="ID de la localidad", description="Identificador único de la localidad.")
    nombre: str = Field(..., title="Nombre de la localidad", description="Nombre oficial de la localidad.")
    provincia_id: int = Field(..., title="ID de la provincia", description="ID de la provincia a la que pertenece la localidad.")
    provincia: Optional[ProvinciaOut] = Field(None, title="Provincia", description="Provincia a la que pertenece la localidad.")

    class Config:
        orm_mode = True
