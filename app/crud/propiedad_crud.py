from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from app.models.propiedad import Propiedad
from app.schemas.propiedad import PropiedadCreate, PropiedadBase

def get_propiedad(db: Session, propiedad_id: int) -> Optional[Propiedad]:
    """
    Obtener una propiedad por su ID.
    """
    return db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()

def get_propiedades(db: Session, skip: int = 0, limit: int = 100) -> List[Propiedad]:
    """
    Obtener todas las propiedades con paginación.
    """
    return db.query(Propiedad).offset(skip).limit(limit).all()

def get_propiedades_by_filters(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[Dict[str, Any]] = None,
    order_by: str = "id",
    order_desc: bool = False
) -> List[Propiedad]:
    """
    Obtener propiedades con filtros y ordenamiento.
    
    Args:
        db: Sesión de la base de datos
        skip: Número de registros a omitir (para paginación)
        limit: Número máximo de registros a devolver
        filters: Diccionario con los filtros a aplicar
        order_by: Campo por el que ordenar los resultados
        order_desc: Si es True, el orden es descendente
    """
    query = db.query(Propiedad)
    
    if filters:
        # Filtro por tipo de propiedad
        if filters.get("tipo_propiedad"):
            query = query.filter(Propiedad.tipo_propiedad == filters["tipo_propiedad"])
        
        # Filtro por tipo de operación
        if filters.get("tipo_operacion"):
            query = query.filter(Propiedad.tipo_operacion == filters["tipo_operacion"])
        
        # Filtro por rango de precios para venta
        if filters.get("precio_min") or filters.get("precio_max"):
            if filters.get("tipo_operacion") == "Venta" or not filters.get("tipo_operacion"):
                if filters.get("precio_min"):
                    query = query.filter(Propiedad.precio_venta >= filters["precio_min"])
                if filters.get("precio_max"):
                    query = query.filter(Propiedad.precio_venta <= filters["precio_max"])
            elif filters.get("tipo_operacion") == "Alquiler":
                if filters.get("precio_min"):
                    query = query.filter(Propiedad.precio_alquiler >= filters["precio_min"])
                if filters.get("precio_max"):
                    query = query.filter(Propiedad.precio_alquiler <= filters["precio_max"])
            else:  # VentaAlquiler u otro
                if filters.get("precio_min"):
                    query = query.filter(
                        or_(
                            Propiedad.precio_venta >= filters["precio_min"],
                            Propiedad.precio_alquiler >= filters["precio_min"]
                        )
                    )
                if filters.get("precio_max"):
                    query = query.filter(
                        or_(
                            Propiedad.precio_venta <= filters["precio_max"],
                            Propiedad.precio_alquiler <= filters["precio_max"]
                        )
                    )
        
        # Filtro por número mínimo de dormitorios
        if filters.get("dormitorios"):
            query = query.filter(Propiedad.dormitorios >= filters["dormitorios"])
        
        # Filtro por número mínimo de baños
        if filters.get("banios"):
            query = query.filter(Propiedad.banios >= filters["banios"])
        
        # Filtro por superficie mínima
        if filters.get("superficie_min"):
            # Superficie total es calculada, así que usamos superficie_cubierta + superficie_descubierta
            query = query.filter(
                func.coalesce(Propiedad.superficie_cubierta, 0) + 
                func.coalesce(Propiedad.superficie_descubierta, 0) >= 
                filters["superficie_min"]
            )
        
        # Filtro por estado
        if filters.get("estado"):
            query = query.filter(Propiedad.estado == filters["estado"])
        
        # Filtro por propietario
        if filters.get("propietario_id"):
            query = query.filter(Propiedad.propietario_id == filters["propietario_id"])
        
        # Filtro por agente
        if filters.get("agente_id"):
            query = query.filter(Propiedad.agente_id == filters["agente_id"])
    
    # Ordenamiento
    column = getattr(Propiedad, order_by, Propiedad.id)
    if order_desc:
        column = column.desc()
    
    query = query.order_by(column)
    
    # Paginación
    return query.offset(skip).limit(limit).all()

def create_propiedad(db: Session, propiedad: PropiedadCreate, agente_id: Optional[int] = None) -> Propiedad:
    """
    Crear una nueva propiedad.
    """
    # Crear un diccionario con los datos de la propiedad
    propiedad_data = propiedad.model_dump()
    
    # Si se proporciona un agente_id, sobrescribir el valor
    if agente_id:
        propiedad_data["agente_id"] = agente_id
    
    # Crear la instancia de Propiedad
    db_propiedad = Propiedad(**propiedad_data)
    
    # Agregar a la sesión y guardar
    db.add(db_propiedad)
    db.commit()
    db.refresh(db_propiedad)
    
    return db_propiedad

def update_propiedad(db: Session, propiedad_id: int, propiedad: Union[PropiedadBase, Dict[str, Any]]) -> Optional[Propiedad]:
    """
    Actualizar una propiedad existente.
    
    Args:
        db: Sesión de la base de datos
        propiedad_id: ID de la propiedad a actualizar
        propiedad: Schema o diccionario con los datos a actualizar
    """
    db_propiedad = get_propiedad(db, propiedad_id=propiedad_id)
    if not db_propiedad:
        return None
    
    # Convertir el schema a diccionario si es necesario
    if hasattr(propiedad, "model_dump"):
        propiedad_data = propiedad.model_dump(exclude_unset=True)
    else:
        propiedad_data = propiedad
    
    # Actualizar la fecha de modificación
    propiedad_data["fecha_modificacion"] = datetime.utcnow()
    
    # Actualizar los campos de la propiedad
    for key, value in propiedad_data.items():
        if hasattr(db_propiedad, key):
            setattr(db_propiedad, key, value)
    
    db.commit()
    db.refresh(db_propiedad)
    
    return db_propiedad

def delete_propiedad(db: Session, propiedad_id: int) -> bool:
    """
    Eliminar una propiedad.
    
    Returns:
        bool: True si se eliminó correctamente, False si no se encontró la propiedad
    """
    db_propiedad = get_propiedad(db, propiedad_id=propiedad_id)
    if not db_propiedad:
        return False
    
    db.delete(db_propiedad)
    db.commit()
    
    return True