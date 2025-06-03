from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Path
from sqlalchemy.orm import Session
from typing import List
import logging # Added import

from app.core.database import get_db
from app.schemas import ( # Changed to app.schemas
    ImagenPropiedadCreate, 
    ImagenAgenteCreate, 
    ImagenPropiedadOut, 
    ImagenAgenteOut,
    ImagenUploadResponse,
    EstablecerImagenPrincipalRequest
)
from app.crud import imagenes as crud_imagenes # Changed to app.crud

# Configurar logger
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(
    prefix="/imagenes",
    tags=["Imágenes"],
    responses={404: {"description": "No encontrado"}},
)

# Rutas para imágenes de propiedades

@router.post("/propiedades/", response_model=ImagenUploadResponse)
async def upload_imagen_propiedad(
    propiedad_id: int = Form(..., description="ID de la propiedad"),
    tipo: str = Form("secundaria", description="Tipo de imagen (ej. 'principal', 'secundaria')"),
    file: UploadFile = File(..., description="Archivo de imagen a subir"),
    db: Session = Depends(get_db)
):
    """
    Sube una nueva imagen para una propiedad.
    
    - **propiedad_id**: ID de la propiedad a la que se asociará la imagen
    - **tipo**: Tipo de imagen (por defecto 'secundaria')  
    - **file**: Archivo de imagen a subir
    """
    try:
        # Validar el tipo de archivo
        content_type = file.content_type or ""
        if not content_type.startswith("image/"):
            raise HTTPException(
                status_code=400, 
                detail="El archivo debe ser una imagen (JPEG, PNG, etc.)"
            )
        
        # Crear el objeto de creación
        imagen_create = ImagenPropiedadCreate(
            propiedad_id=propiedad_id,
            tipo=tipo,
            tipo_imagen="propiedad"
        )
        
        # Guardar la imagen
        result = crud_imagenes.create_imagen_propiedad(db, imagen_create, file)
        return result
    except HTTPException as e:
        # Re-lanzar excepciones HTTP
        raise e
    except Exception as e:
        logger.error(f"Error al subir imagen de propiedad: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error al procesar la imagen: {str(e)}"
        )

@router.get("/propiedades/{imagen_id}", response_model=ImagenPropiedadOut)
def get_imagen_propiedad(
    imagen_id: int = Path(..., description="ID de la imagen a obtener"),
    db: Session = Depends(get_db)
):
    """
    Obtiene una imagen de propiedad por su ID.
    
    - **imagen_id**: ID de la imagen a obtener
    """
    imagen = crud_imagenes.get_imagen_propiedad(db, imagen_id)
    if not imagen:
        raise HTTPException(
            status_code=404, 
            detail=f"Imagen con ID {imagen_id} no encontrada"
        )
    return imagen

@router.get("/propiedades/by-propiedad/{propiedad_id}", response_model=List[ImagenPropiedadOut])
def get_imagenes_propiedad(
    propiedad_id: int = Path(..., description="ID de la propiedad"),
    db: Session = Depends(get_db)
):
    """
    Obtiene todas las imágenes asociadas a una propiedad.
    
    - **propiedad_id**: ID de la propiedad
    """
    return crud_imagenes.get_imagenes_by_propiedad(db, propiedad_id)

@router.put("/propiedades/{propiedad_id}/set-principal", response_model=dict)
def establecer_imagen_principal_propiedad(
    propiedad_id: int = Path(..., description="ID de la propiedad"),
    request: EstablecerImagenPrincipalRequest = None,
    db: Session = Depends(get_db)
):
    """
    Establece una imagen como principal/portada para una propiedad.
    
    - **propiedad_id**: ID de la propiedad
    - **request.imagen_id**: ID de la imagen que será establecida como principal
    """
    if not request or not request.imagen_id:
        raise HTTPException(
            status_code=400, 
            detail="Se requiere el ID de la imagen"
        )
    
    result = crud_imagenes.set_imagen_principal_propiedad(db, propiedad_id, request.imagen_id)
    return {"success": result, "message": "Imagen establecida como principal correctamente"}

@router.delete("/propiedades/{imagen_id}", response_model=dict)
def delete_imagen_propiedad(
    imagen_id: int = Path(..., description="ID de la imagen a eliminar"),
    db: Session = Depends(get_db)
):
    """
    Elimina una imagen de propiedad.
    
    - **imagen_id**: ID de la imagen a eliminar
    """
    result = crud_imagenes.delete_imagen_propiedad(db, imagen_id)
    if not result:
        raise HTTPException(
            status_code=404, 
            detail=f"Imagen con ID {imagen_id} no encontrada"
        )
    return {"success": True, "message": "Imagen eliminada correctamente"}

# Rutas para imágenes de agentes

@router.post("/agentes/", response_model=ImagenUploadResponse)
async def upload_imagen_agente(
    agente_id: int = Form(..., description="ID del agente"),
    tipo: str = Form("secundaria", description="Tipo de imagen (ej. 'principal', 'perfil', 'secundaria')"),
    file: UploadFile = File(..., description="Archivo de imagen a subir"),
    db: Session = Depends(get_db)
):
    """
    Sube una nueva imagen para un agente.
    
    - **agente_id**: ID del agente al que se asociará la imagen
    - **tipo**: Tipo de imagen (por defecto 'secundaria')
    - **file**: Archivo de imagen a subir
    """
    try:
        # Validar el tipo de archivo
        content_type = file.content_type or ""
        if not content_type.startswith("image/"):
            raise HTTPException(
                status_code=400, 
                detail="El archivo debe ser una imagen (JPEG, PNG, etc.)"
            )
        
        # Crear el objeto de creación
        imagen_create = ImagenAgenteCreate(
            agente_id=agente_id,
            tipo=tipo,
            tipo_imagen="agente"
        )
        
        # Guardar la imagen
        result = crud_imagenes.create_imagen_agente(db, imagen_create, file)
        return result
    except HTTPException as e:
        # Re-lanzar excepciones HTTP
        raise e
    except Exception as e:
        logger.error(f"Error al subir imagen de agente: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error al procesar la imagen: {str(e)}"
        )

@router.get("/agentes/{imagen_id}", response_model=ImagenAgenteOut)
def get_imagen_agente(
    imagen_id: int = Path(..., description="ID de la imagen a obtener"),
    db: Session = Depends(get_db)
):
    """
    Obtiene una imagen de agente por su ID.
    
    - **imagen_id**: ID de la imagen a obtener
    """
    imagen = crud_imagenes.get_imagen_agente(db, imagen_id)
    if not imagen:
        raise HTTPException(
            status_code=404, 
            detail=f"Imagen con ID {imagen_id} no encontrada"
        )
    return imagen

@router.get("/agentes/by-agente/{agente_id}", response_model=List[ImagenAgenteOut])
def get_imagenes_agente(
    agente_id: int = Path(..., description="ID del agente"),
    db: Session = Depends(get_db)
):
    """
    Obtiene todas las imágenes asociadas a un agente.
    
    - **agente_id**: ID del agente
    """
    return crud_imagenes.get_imagenes_by_agente(db, agente_id)

@router.put("/agentes/{agente_id}/set-principal", response_model=dict)
def establecer_imagen_principal_agente(
    agente_id: int = Path(..., description="ID del agente"),
    request: EstablecerImagenPrincipalRequest = None,
    db: Session = Depends(get_db)
):
    """
    Establece una imagen como principal/perfil para un agente.
    
    - **agente_id**: ID del agente
    - **request.imagen_id**: ID de la imagen que será establecida como principal
    """
    if not request or not request.imagen_id:
        raise HTTPException(
            status_code=400, 
            detail="Se requiere el ID de la imagen"
        )
    
    result = crud_imagenes.set_imagen_principal_agente(db, agente_id, request.imagen_id)
    return {"success": result, "message": "Imagen establecida como principal correctamente"}

@router.delete("/agentes/{imagen_id}", response_model=dict)
def delete_imagen_agente(
    imagen_id: int = Path(..., description="ID de la imagen a eliminar"),
    db: Session = Depends(get_db)
):
    """
    Elimina una imagen de agente.
    
    - **imagen_id**: ID de la imagen a eliminar
    """
    result = crud_imagenes.delete_imagen_agente(db, imagen_id)
    if not result:
        raise HTTPException(
            status_code=404, 
            detail=f"Imagen con ID {imagen_id} no encontrada"
        )
    return {"success": True, "message": "Imagen eliminada correctamente"}