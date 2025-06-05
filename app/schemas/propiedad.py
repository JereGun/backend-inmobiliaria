from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.models.enums import TipoPropiedadEnum, TipoOperacionEnum, EstadoEnum
from app.schemas.direccion import DireccionOut
from app.schemas.cliente import ClienteOut
from app.schemas.agente import Agente # Changed from AgenteOut
from app.schemas.direccion import DireccionCreateNested


class PropiedadBase(BaseModel):
    nombre: str = Field(..., title="Nombre de la propiedad", description="Nombre de la propiedad")
    tipo_propiedad: TipoPropiedadEnum = Field(..., title="Tipo de propiedad", description="Tipo de propiedad (ej. 'Casa', 'Departamento', etc.)")
    tipo_operacion: TipoOperacionEnum = Field(..., title="Tipo de operación", description="Tipo de operación (ej. 'Alquiler', 'Venta', etc.)")
    precio_venta: Optional[int] = Field(None, title="Precio de venta", description="Precio de venta de la propiedad")
    precio_alquiler: Optional[int] = Field(None, title="Precio de alquiler", description="Precio de alquiler de la propiedad")
    descripcion: Optional[str] = Field(None, title="Descripción", description="Descripción de la propiedad")
    ano_construccion: Optional[int] = Field(None, title="Año de construcción", description="Año de construcción de la propiedad")
    banios: Optional[int] = Field(None, title="Número de baños", description="Número de baños en la propiedad")
    dormitorios: Optional[int] = Field(None, title="Número de dormitorios", description="Número de dormitorios en la propiedad")
    ambientes: Optional[int] = Field(None, title="Número de ambientes", description="Número de ambientes en la propiedad")
    cochera: Optional[int] = Field(None, title="Número de cocheras", description="Número de cocheras en la propiedad")
    amoblado: Optional[bool] = Field(None, title="Amoblado", description="Indica si la propiedad está amoblada o no")
    superficie_cubierta: Optional[int] = Field(None, title="Superficie cubierta", description="Superficie cubierta en m2")
    superficie_descubierta: Optional[int] = Field(None, title="Superficie descubierta", description="Superficie descubierta en m2")
    estado: EstadoEnum = Field(EstadoEnum.borrador, title="Estado", description="Estado de la propiedad (ej. 'Borrador', 'Publicada', etc.)")
    direccion_id: int = Field(..., title="ID de la dirección", description="ID de la dirección de la propiedad")  # Cambio a obligatorio
    propietario_id: Optional[int] = Field(None, title="ID del propietario", description="ID del propietario de la propiedad")
    agente_id: Optional[int] = Field(None, title="ID del agente", description="ID del agente a cargo de la propiedad")
    portada_id: Optional[int] = Field(None, title="ID de la portada", description="ID de la imagen de portada de la propiedad")

    @field_validator('precio_venta')
    def validate_precio_venta(cls, v, values):
        tipo_operacion = values.get('tipo_operacion')
        if tipo_operacion in ['Venta', 'VentaAlquiler'] and v is None:
            raise ValueError('El precio de venta es obligatorio para propiedades en venta')
        return v

    @field_validator('precio_alquiler')
    def validate_precio_alquiler(cls, v, values):
        tipo_operacion = values.get('tipo_operacion')
        if tipo_operacion in ['Alquiler', 'VentaAlquiler'] and v is None:
            raise ValueError('El precio de alquiler es obligatorio para propiedades en alquiler')
        return v

    @property
    def superficie_total(self) -> Optional[int]:
        """Calcula la superficie total sumando las superficies cubierta y descubierta"""
        if self.superficie_cubierta is None and self.superficie_descubierta is None:
            return None
        total = 0
        if self.superficie_cubierta is not None:
            total += self.superficie_cubierta
        if self.superficie_descubierta is not None:
            total += self.superficie_descubierta
        return total
    
class PropiedadCreate(PropiedadBase):
    """Esquema para crear una nueva propiedad"""
    direccion: Optional[DireccionCreateNested] = Field(None, title="Dirección de la propiedad", description="Dirección de la propiedad para crear")

class PropiedadOut(PropiedadBase):
    id: int = Field(..., title="ID de la propiedad", description="Identificador único de la propiedad")
    fecha_creacion: datetime = Field(..., title="Fecha de creación", description="Fecha de creación de la propiedad")
    fecha_modificacion: Optional[datetime] = Field(None, title="Fecha de modificación", description="Fecha de última modificación de la propiedad")
    direccion: Optional[DireccionOut] = Field(None, title="Dirección", description="Dirección asociada a la propiedad")
    propietario: Optional[ClienteOut] = Field(None, title="Propietario", description="Propietario asociado a la propiedad")
    agente: Optional[Agente] = Field(None, title="Agente", description="Agente asociado a la propiedad") # Changed from AgenteOut
    
    @property
    def superficie_total(self) -> Optional[int]:
        """Calcula la superficie total sumando las superficies cubierta y descubierta"""
        if self.superficie_cubierta is None and self.superficie_descubierta is None:
            return None
        total = 0
        if self.superficie_cubierta is not None:
            total += self.superficie_cubierta
        if self.superficie_descubierta is not None:
            total += self.superficie_descubierta
        return total

    model_config = {
        "from_attributes": True
    }