from pydantic import BaseModel, Field, field_validator
from typing import Optional

# TODO Pais-Schema
class PaisBase(BaseModel):
    nombre: str = Field(..., title="Nombre del pais", description="Nombre oficial del pais en español")

class PaisCreate(PaisBase):
    """Esquema para crear un nuevo pais"""
    pass

class PaisOut(PaisBase):
    id: int = Field(..., title="ID del pais", description="Identificador unico del pais")
    
    model_config = {
        "from_attributes": True
    }

# TODO Provincia-Schema
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

    model_config = {
        "from_attributes": True
    }



# TODO Localidad-Schema
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

    model_config = {
        "from_attributes": True
    }


# TODO Direccion-Schema
class DireccionBase(BaseModel):
    """Esquema base para representar una direccion."""
    calle: str = Field(..., title="Calle", description="Nombre de la calle")
    altura: int = Field(..., title="Altura", description="Numero de la calle")
    codigo_postal: int = Field(..., title="Codigo Postal", description="Codigo postal de la direccion")
    barrio: str = Field(..., title="Barrio", description="Nombre del barrio")
    localidad_id: int = Field(..., title="ID de la localidad", description="ID de la localidad a la que pertenece la direccion.")
    provincia_id: int = Field(..., title="ID de la provincia", description="ID de la provincia a la que pertenece la direccion.")
    pais_id: int = Field(..., title="ID del pais", description="ID del pais al que pertenece la direccion.")

    @field_validator("altura")
    def validar_altura(cls, value):
        if value <= 0:
            raise ValueError("La altura debe ser un número positivo.")
        return value
    
class DireccionCreate(DireccionBase):
    """Esquema para crear una nueva direccion"""
    pass

class DireccionOut(DireccionBase):
    id: int = Field(..., title="ID de la direccion", description="Identificador unico de la direccion")
    calle: str = Field(..., title="Calle", description="Nombre de la calle")
    altura: int = Field(..., title="Altura", description="Numero de la calle")
    piso: Optional[str] = Field(None, title="Piso", description="Numero de piso de la direccion")
    dpto: Optional[str] = Field(None, title="Departamento", description="Numero de departamento de la direccion")
    entre_calles: Optional[str] = Field(None, title="Entre calles", description="Nombre de las calles entre las que se encuentra la direccion")
    observaciones: Optional[str] = Field(None, title="Observaciones", description="Observaciones adicionales sobre la direccion")
    codigo_postal: int = Field(..., title="Codigo Postal", description="Codigo postal de la direccion")
    barrio: str = Field(..., title="Barrio", description="Nombre del barrio")
    localidad_id: int = Field(..., title="ID de la localidad", description="ID de la localidad a la que pertenece la direccion.")
    provincia_id: int = Field(..., title="ID de la provincia", description="ID de la provincia a la que pertenece la direccion.")
    pais_id: int = Field(..., title="ID del pais", description="ID del pais al que pertenece la direccion.")

    model_config = {
        "from_attributes": True
    }
