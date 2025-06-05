from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.core.database import get_db  # Corrected import
from app.core.auth import get_current_user  # Corrected import
from app.models.usuario import Usuario as User # Corrected import
from app.models.propiedad import Propiedad
from app.schemas.propiedad import PropiedadCreate, PropiedadOut, PropiedadBase
from app.crud.propiedad_crud import ( # Corrected module name
    create_propiedad,
    get_propiedad,
    get_propiedades,
    update_propiedad,
    delete_propiedad,
    get_propiedades_by_filters
)

router = APIRouter(
    prefix="/propiedades",
    tags=["propiedades"],
    responses={404: {"description": "Propiedad no encontrada"}},
)


@router.post("/", response_model=PropiedadOut, status_code=status.HTTP_201_CREATED)
def create_propiedad_endpoint(
    propiedad: PropiedadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crear una nueva propiedad.
    
    Requiere autenticación.
    """
    # Si el usuario no es un agente o administrador, no puede crear propiedades
    if not (current_user.is_admin or current_user.is_agente):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear propiedades"
        )
    
    # Asignar el agente automáticamente si el usuario es un agente y no se especificó
    if current_user.is_agente and not propiedad.agente_id:
        agente_id = current_user.agente_id
    else:
        agente_id = propiedad.agente_id
    
    # Validar precios según tipo de operación
    if propiedad.tipo_operacion == "Venta" and not propiedad.precio_venta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio de venta es obligatorio para propiedades en venta"
        )
    
    if propiedad.tipo_operacion == "Alquiler" and not propiedad.precio_alquiler:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio de alquiler es obligatorio para propiedades en alquiler"
        )
    
    if propiedad.tipo_operacion == "VentaAlquiler" and (not propiedad.precio_venta or not propiedad.precio_alquiler):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los precios de venta y alquiler son obligatorios para propiedades en venta/alquiler"
        )
    
    return create_propiedad(db=db, propiedad=propiedad, agente_id=agente_id)


@router.get("/", response_model=List[PropiedadOut])
def read_propiedades(
    skip: int = 0,
    limit: int = 100,
    tipo_propiedad: Optional[str] = Query(None, description="Filtrar por tipo de propiedad"),
    tipo_operacion: Optional[str] = Query(None, description="Filtrar por tipo de operación"),
    precio_min: Optional[int] = Query(None, description="Precio mínimo"),
    precio_max: Optional[int] = Query(None, description="Precio máximo"),
    dormitorios: Optional[int] = Query(None, description="Número mínimo de dormitorios"),
    banios: Optional[int] = Query(None, description="Número mínimo de baños"),
    superficie_min: Optional[int] = Query(None, description="Superficie mínima total en m2"),
    estado: Optional[str] = Query(None, description="Estado de la propiedad"),
    propietario_id: Optional[int] = Query(None, description="ID del propietario"),
    agente_id: Optional[int] = Query(None, description="ID del agente"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Obtener todas las propiedades con filtros opcionales.
    
    Si el usuario no está autenticado, solo puede ver propiedades publicadas.
    """
    
    # Para usuarios no autenticados o clientes regulares, mostrar solo propiedades publicadas
    if not current_user or (not current_user.is_admin and not current_user.is_agente):
        estado = "PUBLICADA"
    
    # Para agentes, si no se especifica un filtro de agente_id, mostrar solo sus propiedades
    elif current_user.is_agente and not agente_id and not current_user.is_admin:
        agente_id = current_user.agente_id
    
    filters = {
        "tipo_propiedad": tipo_propiedad,
        "tipo_operacion": tipo_operacion,
        "precio_min": precio_min,
        "precio_max": precio_max,
        "dormitorios": dormitorios,
        "banios": banios,
        "superficie_min": superficie_min,
        "estado": estado,
        "propietario_id": propietario_id,
        "agente_id": agente_id
    }
    
    propiedades = get_propiedades_by_filters(db, skip=skip, limit=limit, filters=filters)
    return propiedades


@router.get("/{propiedad_id}", response_model=PropiedadOut)
def read_propiedad(
    propiedad_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Obtener una propiedad específica por su ID.
    
    Si el usuario no está autenticado, solo puede ver propiedades publicadas.
    """
    propiedad = get_propiedad(db, propiedad_id=propiedad_id)
    if not propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    
    # Verificar permisos
    if propiedad.estado != "PUBLICADA":
        if not current_user:
            raise HTTPException(status_code=403, detail="No tienes permisos para ver esta propiedad")
        
        # Admin puede ver todo
        if current_user.is_admin:
            return propiedad
            
        # Agente puede ver sus propias propiedades o propiedades publicadas
        if current_user.is_agente and propiedad.agente_id == current_user.agente_id:
            return propiedad
            
        # Propietario puede ver sus propias propiedades
        if propiedad.propietario_id == current_user.id:
            return propiedad
            
        raise HTTPException(status_code=403, detail="No tienes permisos para ver esta propiedad")
    
    return propiedad


@router.put("/{propiedad_id}", response_model=PropiedadOut)
def update_propiedad_endpoint(
    propiedad_id: int,
    propiedad: PropiedadBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar una propiedad existente.
    
    Requiere autenticación. Solo el agente asignado, el propietario o un administrador 
    pueden actualizar la propiedad.
    """
    db_propiedad = get_propiedad(db, propiedad_id=propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    
    # Verificar permisos
    if not current_user.is_admin:
        if current_user.is_agente and db_propiedad.agente_id != current_user.agente_id:
            raise HTTPException(status_code=403, detail="No tienes permisos para actualizar esta propiedad")
        elif not current_user.is_agente and db_propiedad.propietario_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tienes permisos para actualizar esta propiedad")
    
    # Validar precios según tipo de operación
    if propiedad.tipo_operacion == "Venta" and not propiedad.precio_venta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio de venta es obligatorio para propiedades en venta"
        )
    
    if propiedad.tipo_operacion == "Alquiler" and not propiedad.precio_alquiler:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio de alquiler es obligatorio para propiedades en alquiler"
        )
    
    if propiedad.tipo_operacion == "VentaAlquiler" and (not propiedad.precio_venta or not propiedad.precio_alquiler):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los precios de venta y alquiler son obligatorios para propiedades en venta/alquiler"
        )
    
    return update_propiedad(db=db, propiedad_id=propiedad_id, propiedad=propiedad)


@router.delete("/{propiedad_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_propiedad_endpoint(
    propiedad_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Eliminar una propiedad.
    
    Requiere autenticación. Solo un administrador puede eliminar una propiedad.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar propiedades"
        )
    
    db_propiedad = get_propiedad(db, propiedad_id=propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    
    delete_propiedad(db=db, propiedad_id=propiedad_id)
    return None


@router.patch("/{propiedad_id}/estado", response_model=PropiedadOut)
def update_estado_propiedad(
    propiedad_id: int,
    estado: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar el estado de una propiedad.
    
    Requiere autenticación. Solo el agente asignado o un administrador pueden cambiar el estado.
    """
    if not (current_user.is_admin or current_user.is_agente):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar el estado de propiedades"
        )
    
    db_propiedad = get_propiedad(db, propiedad_id=propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    
    # Si es agente, verificar que sea el asignado a la propiedad
    if current_user.is_agente and not current_user.is_admin:
        if db_propiedad.agente_id != current_user.agente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo puedes actualizar el estado de tus propiedades asignadas"
            )
    
    # Validar que el estado sea válido
    valid_estados = ["BORRADOR", "REVISION", "PUBLICADA", "PAUSADA", "VENDIDA", "ALQUILADA", "CANCELADA"]
    if estado not in valid_estados:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Estado inválido. Estados válidos: {', '.join(valid_estados)}"
        )
    
    # Actualizar solo el estado
    return update_propiedad(db=db, propiedad_id=propiedad_id, propiedad={"estado": estado})


@router.get("/destacadas/", response_model=List[PropiedadOut])
def get_propiedades_destacadas(
    limit: int = 6,
    db: Session = Depends(get_db)
):
    """
    Obtener propiedades destacadas para mostrar en la página principal.
    
    Devuelve propiedades publicadas, ordenadas por fecha de creación (más recientes primero).
    """
    filters = {
        "estado": "PUBLICADA"
    }
    
    propiedades = get_propiedades_by_filters(
        db, 
        skip=0, 
        limit=limit, 
        filters=filters,
        order_by="fecha_creacion",
        order_desc=True
    )
    
    return propiedades


@router.get("/por-agente/{agente_id}", response_model=List[PropiedadOut])
def get_propiedades_por_agente(
    agente_id: int,
    estado: Optional[str] = Query(None, description="Estado de la propiedad"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Obtener propiedades asignadas a un agente específico.
    
    Si el usuario no está autenticado, solo puede ver propiedades publicadas.
    """
    # Para usuarios no autenticados o clientes regulares, mostrar solo propiedades publicadas
    if not current_user or (not current_user.is_admin and not current_user.is_agente):
        estado = "PUBLICADA"
    
    filters = {
        "agente_id": agente_id,
        "estado": estado
    }
    
    propiedades = get_propiedades_by_filters(db, skip=skip, limit=limit, filters=filters)
    return propiedades


@router.get("/por-propietario/{propietario_id}", response_model=List[PropiedadOut])
def get_propiedades_por_propietario(
    propietario_id: int,
    estado: Optional[str] = Query(None, description="Estado de la propiedad"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener propiedades de un propietario específico.
    
    Requiere autenticación. Solo el propietario, su agente asignado o un administrador 
    pueden ver todas las propiedades del propietario.
    """
    # Verificar permisos
    if not current_user.is_admin:
        if current_user.id != propietario_id:
            # Si es agente, verificar si tiene acceso a las propiedades de este propietario
            if current_user.is_agente:
                # Verificar si tiene alguna propiedad asignada de este propietario
                propiedad = db.query(Propiedad).filter(
                    and_(
                        Propiedad.propietario_id == propietario_id,
                        Propiedad.agente_id == current_user.agente_id
                    )
                ).first()
                
                if not propiedad:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="No tienes permisos para ver las propiedades de este propietario"
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para ver las propiedades de este propietario"
                )
    
    filters = {
        "propietario_id": propietario_id,
        "estado": estado
    }
    
    propiedades = get_propiedades_by_filters(db, skip=skip, limit=limit, filters=filters)
    return propiedades