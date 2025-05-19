from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum as SQLAlchemyEnum
from app.database import Base
from enum import Enum

class TipoPropeidadEnum(str, Enum):
    casa = "Casa"
    departamento = "Departamento"
    oficina = "Oficina"
    local_comercial = "Local Comercial"
    terreno = "Terreno"
    cochera = "Cochera"
    galpon = "Galpon"
    otro = "Otro"

class TipoOperacionEnum(str, Enum):
    venta = "Venta"
    alquiler = "Alquiler"
    ambos = "Ambos"

class EstadoEnum(str, Enum):
    borrador = "Borrador"
    activo = "Activo"
    inactivo = "Inactivo"
    reservado = "Reservado"
    vendido = "Vendido"
    alquilado = "Alquilado"
    borrador = "Borrador"

#   id integer
#   name varchar
#   property_type_id integer [ref: > property_type.id, note: "house, apartment, business, etc."]
#   address_id integer [ref: - address.id]
#   owner_id integer [ref: > customer.id, note: "owner or tenant"]
#   bathrooms integer
#   bedrooms integer
#   rooms integer
#   garage integer
#   furnished bool
#   sale_rent string
#   price_rent integer
#   price_sale integer
#   status_id integer [ref: > property_status.id]
#   covered_surface integer
#   uncovered_surface integer
#   total_surface integer [note: 'covered_surface + uncovered_surface']
#   agent_id integer [ref: > agent.id]
#   description text
#   created_at timestamp
#   update_at timestamp

class Propiedad (Base):
    __tablename__ = "propiedades"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    direccion_id = Column(Integer, ForeignKey("direcciones.id"), nullable=False) # Direccion FK
    tipo_propiedad = Column(SQLAlchemyEnum(TipoPropeidadEnum, name="tipo_documento_enum"), nullable=False, default=TipoPropeidadEnum.casa)
    tipo_operacion = Column(SQLAlchemyEnum(TipoOperacionEnum, name="tipo_documento_enum"), nullable=False, default=TipoOperacionEnum.alquiler)
    precio_venta = Column(Integer, nullable=True)
    precio_alquiler = Column(Integer, nullable=True)
    propietario_id = Column(Integer, ForeignKey("clientes.id"), nullable=True) # Cliente FK
    estado = Column(SQLAlchemyEnum(EstadoEnum, name="estado_enum"), nullable=False, default=EstadoEnum.borrador)
    descripcion = Column(String, nullable=True)
    # Caracteristicas
    banios = Column(Integer, nullable=True)
    dormitorios = Column(Integer, nullable=True)
    ambientes = Column(Integer, nullable=True)
    cochera = Column(Integer, nullable=True)
    amoblado = Column(Boolean, nullable=True)
    superficie_cubierta = Column(Integer, nullable=True)
    superficie_descubierta = Column(Integer, nullable=True)
    superficie_total = Column(Integer, nullable=True, default=superficie_cubierta + superficie_descubierta)
    agente_id = Column(Integer, ForeignKey("agente.id"), nullable=True) # Agente FK
    