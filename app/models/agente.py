from app.core.database import Base
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, DateTime
from app.models.enums import tipo_documento_enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .usuario import Usuario # Import Usuario

class Agente(Usuario): # Inherit from Usuario
    __tablename__ = "agentes"

    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True) # ForeignKey to usuarios.id
    # email field is removed (inherited from Usuario)
    # is_active field from Usuario can be used, so 'activo' could be removed or its logic re-evaluated.
    # For now, let's assume 'activo' in Agente might have a different meaning than Usuario.is_active,
    # so we'll keep it. If they are the same, 'activo' should be removed from Agente.

    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    tipo_documento = Column(tipo_documento_enum, nullable=False, default="DNI")
    numero_documento = Column(String, unique=True, index=True)
    telefono = Column(String, nullable=False)
    fecha_nacimiento = Column(DateTime, nullable=False)
    activo = Column(Boolean, default=True) # Keeping this for now.
    direccion_id = Column(Integer, ForeignKey("direcciones.id"), nullable=True)
    licencia = Column(String, nullable=False)
    fecha_alta = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, nullable=True)

    # Relaciones
    # The 'usuario' relationship can be established using the joined table inheritance.
    # SQLAlchemy handles this automatically for the fields inherited from Usuario.
    # If a direct reference to the Usuario part is needed, it can be accessed via the Agente instance itself.

    direccion = relationship("Direccion", back_populates="agentes")
    propiedades = relationship("Propiedad", back_populates="agente")
    # Assuming ImagenAgente is specific to Agente and not all Usuarios.
    # If ImagenAgente needs to link to the 'agentes' table's primary key (which is now users.id),
    # ensure its ForeignKey points to 'agentes.id' or 'usuarios.id' as appropriate.
    # For now, assuming 'ImagenAgente' has a ForeignKey to 'agentes.id'.
    imagenes = relationship("ImagenAgente", back_populates="agente")

    # Add a back_populates for the one-to-one relationship with Usuario if needed for queries,
    # though SQLAlchemy's joined table inheritance usually handles this transparently.
    # For example, if you had a 'agente_profile' on Usuario:
    # usuario = relationship("Usuario", back_populates="agente_profile")
    # But since Agente IS a Usuario, this might not be necessary.
