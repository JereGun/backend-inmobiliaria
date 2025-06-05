from typing import Optional, List, Literal # Added Literal
from pydantic import BaseModel, HttpUrl, Field, field_validator
from datetime import datetime

# Base para todas las imágenes
class ImagenBase(BaseModel):
    url: str = Field(..., title="URL de la imagen", description="URL o ruta donde se almacena la imagen")
    tipo: str = Field(..., title="Tipo de imagen", description="Tipo de imagen (ej. 'principal', 'secundaria', 'perfil')")

    @field_validator('url')
    def validate_url(cls, v):
        # Si la URL no tiene http/https, asumimos que es una ruta local
        if not v.startswith(('http://', 'https://')):
            # Validar que no haya caracteres sospechosos en la ruta
            invalid_chars = ['..', ';', '&', '|', '>', '<']
            if any(char in v for char in invalid_chars):
                raise ValueError("La URL o ruta contiene caracteres no permitidos")
        return v

class ImagenCreate(ImagenBase):
    """Esquema base para crear una nueva imagen"""
    # La URL se generará automáticamente al subir el archivo
    url: Optional[str] = Field(None, title="URL de la imagen", 
                              description="Este campo se genera automáticamente al subir la imagen")
    
    class Config:
        # Permitir que el campo url sea None al crear
        # Se generará al guardar el archivo
        extra = "allow"

class ImagenOut(ImagenBase):
    """Esquema base para mostrar una imagen"""
    id: int = Field(..., title="ID de la imagen", description="Identificador único de la imagen")
    
    class Config:
        from_attributes = True

# Para propiedades
class ImagenPropiedadCreate(ImagenCreate):
    """Esquema para crear una nueva imagen de propiedad"""
    propiedad_id: int = Field(..., title="ID de la propiedad", 
                             description="ID de la propiedad a la que pertenece la imagen")
    tipo_imagen: Literal["propiedad"] = "propiedad" # Changed to Literal

class ImagenPropiedadOut(ImagenOut):
    """Esquema para mostrar una imagen de propiedad"""
    propiedad_id: int = Field(..., title="ID de la propiedad", 
                             description="ID de la propiedad a la que pertenece la imagen")

# Para agentes
class ImagenAgenteCreate(ImagenCreate):
    """Esquema para crear una nueva imagen de agente"""
    agente_id: int = Field(..., title="ID del agente", 
                          description="ID del agente al que pertenece la imagen")
    tipo_imagen: Literal["agente"] = "agente" # Changed to Literal

class ImagenAgenteOut(ImagenOut):
    """Esquema para mostrar una imagen de agente"""
    agente_id: int = Field(..., title="ID del agente", 
                          description="ID del agente al que pertenece la imagen")

# Esquema para respuesta de carga de imagen
class ImagenUploadResponse(BaseModel):
    """Esquema para respuesta de carga de imagen"""
    id: int = Field(..., title="ID de la imagen", description="ID de la imagen subida")
    url: str = Field(..., title="URL de la imagen", description="URL para acceder a la imagen")
    tipo: str = Field(..., title="Tipo de imagen", description="Tipo de imagen")
    timestamp: datetime = Field(default_factory=datetime.now, title="Marca de tiempo", 
                               description="Fecha y hora de la subida")

# Esquema para establecer imagen como principal/portada
class EstablecerImagenPrincipalRequest(BaseModel):
    """Esquema para establecer una imagen como principal/portada"""
    imagen_id: int = Field(..., title="ID de la imagen",
                          description="ID de la imagen que será establecida como principal/portada")