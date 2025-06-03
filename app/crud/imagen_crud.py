from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, UploadFile
import os
from datetime import datetime
import shutil
import uuid
from typing import Optional, List

from app.models.imagen import Imagen, ImagenPropiedad, ImagenAgente
from app.schemas.imagen import (
    ImagenPropiedadCreate, 
    ImagenAgenteCreate, 
    ImagenPropiedadOut, 
    ImagenAgenteOut,
    ImagenUploadResponse
)

# Configuración base para almacenamiento de imágenes
UPLOAD_DIRECTORY = "static/uploads"
BASE_URL = "/static/uploads"  # URL base para acceder a las imágenes

# Asegurar que el directorio de uploads existe
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(f"{UPLOAD_DIRECTORY}/propiedades", exist_ok=True)
os.makedirs(f"{UPLOAD_DIRECTORY}/agentes", exist_ok=True)

def save_upload_file(upload_file: UploadFile, folder: str) -> str:
    """Guarda un archivo subido en el directorio especificado"""
    # Crear nombre de archivo único
    file_extension = os.path.splitext(upload_file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Crear la ruta completa
    file_path = os.path.join(UPLOAD_DIRECTORY, folder, unique_filename)
    
    # Guardar el archivo
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()
    
    # Devolver la URL relativa
    return f"{BASE_URL}/{folder}/{unique_filename}"

# CRUD para ImagenPropiedad

def create_imagen_propiedad(
    db: Session, 
    imagen_create: ImagenPropiedadCreate, 
    file: UploadFile
) -> ImagenUploadResponse:
    """Crea una nueva imagen para una propiedad"""
    try:
        # Guardar archivo físicamente
        url = save_upload_file(file, "propiedades")
        
        # Crear registro en la base de datos
        db_imagen = ImagenPropiedad(
            url=url,
            tipo=imagen_create.tipo,
            tipo_imagen="propiedad",
            propiedad_id=imagen_create.propiedad_id
        )
        db.add(db_imagen)
        db.commit()
        db.refresh(db_imagen)
        
        # Devolver respuesta
        return ImagenUploadResponse(
            id=db_imagen.id,
            url=url,
            tipo=db_imagen.tipo,
            timestamp=datetime.now()
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear imagen: {str(e)}")

def get_imagen_propiedad(db: Session, imagen_id: int) -> Optional[ImagenPropiedad]:
    """Obtiene una imagen de propiedad por su ID"""
    return db.query(ImagenPropiedad).filter(ImagenPropiedad.id == imagen_id).first()

def get_imagenes_by_propiedad(db: Session, propiedad_id: int) -> List[ImagenPropiedad]:
    """Obtiene todas las imágenes asociadas a una propiedad"""
    return db.query(ImagenPropiedad).filter(ImagenPropiedad.propiedad_id == propiedad_id).all()

def set_imagen_principal_propiedad(db: Session, propiedad_id: int, imagen_id: int) -> bool:
    """Establece una imagen como principal para una propiedad"""
    try:
        # Primero, establecer todas las imágenes como no principales
        imagenes = db.query(ImagenPropiedad).filter(
            ImagenPropiedad.propiedad_id == propiedad_id
        ).all()
        
        for img in imagenes:
            if img.tipo == "principal":
                img.tipo = "secundaria"
        
        # Establecer la imagen seleccionada como principal
        imagen = db.query(ImagenPropiedad).filter(
            ImagenPropiedad.id == imagen_id,
            ImagenPropiedad.propiedad_id == propiedad_id
        ).first()
        
        if not imagen:
            raise HTTPException(
                status_code=404, 
                detail=f"Imagen con ID {imagen_id} no encontrada para la propiedad {propiedad_id}"
            )
        
        imagen.tipo = "principal"
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")

def update_imagen_propiedad(
    db: Session, 
    imagen_id: int, 
    tipo: str
) -> Optional[ImagenPropiedad]:
    """Actualiza los datos de una imagen de propiedad"""
    db_imagen = get_imagen_propiedad(db, imagen_id)
    if not db_imagen:
        return None
    
    db_imagen.tipo = tipo
    db.commit()
    db.refresh(db_imagen)
    return db_imagen

def delete_imagen_propiedad(db: Session, imagen_id: int) -> bool:
    """Elimina una imagen de propiedad"""
    db_imagen = get_imagen_propiedad(db, imagen_id)
    if not db_imagen:
        return False
    
    # Eliminar el archivo físico si es posible
    try:
        file_path = os.path.join(os.getcwd(), db_imagen.url.lstrip('/'))
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        # Si no se puede eliminar el archivo, continuamos de todas formas
        pass
    
    db.delete(db_imagen)
    db.commit()
    return True

# CRUD para ImagenAgente

def create_imagen_agente(
    db: Session, 
    imagen_create: ImagenAgenteCreate, 
    file: UploadFile
) -> ImagenUploadResponse:
    """Crea una nueva imagen para un agente"""
    try:
        # Guardar archivo físicamente
        url = save_upload_file(file, "agentes")
        
        # Crear registro en la base de datos
        db_imagen = ImagenAgente(
            url=url,
            tipo=imagen_create.tipo,
            tipo_imagen="agente",
            agente_id=imagen_create.agente_id
        )
        db.add(db_imagen)
        db.commit()
        db.refresh(db_imagen)
        
        # Devolver respuesta
        return ImagenUploadResponse(
            id=db_imagen.id,
            url=url,
            tipo=db_imagen.tipo,
            timestamp=datetime.now()
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear imagen: {str(e)}")

def get_imagen_agente(db: Session, imagen_id: int) -> Optional[ImagenAgente]:
    """Obtiene una imagen de agente por su ID"""
    return db.query(ImagenAgente).filter(ImagenAgente.id == imagen_id).first()

def get_imagenes_by_agente(db: Session, agente_id: int) -> List[ImagenAgente]:
    """Obtiene todas las imágenes asociadas a un agente"""
    return db.query(ImagenAgente).filter(ImagenAgente.agente_id == agente_id).all()

def set_imagen_principal_agente(db: Session, agente_id: int, imagen_id: int) -> bool:
    """Establece una imagen como principal para un agente"""
    try:
        # Primero, establecer todas las imágenes como no principales
        imagenes = db.query(ImagenAgente).filter(
            ImagenAgente.agente_id == agente_id
        ).all()
        
        for img in imagenes:
            if img.tipo == "principal":
                img.tipo = "secundaria"
        
        # Establecer la imagen seleccionada como principal
        imagen = db.query(ImagenAgente).filter(
            ImagenAgente.id == imagen_id,
            ImagenAgente.agente_id == agente_id
        ).first()
        
        if not imagen:
            raise HTTPException(
                status_code=404, 
                detail=f"Imagen con ID {imagen_id} no encontrada para el agente {agente_id}"
            )
        
        imagen.tipo = "principal"
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")

def update_imagen_agente(
    db: Session, 
    imagen_id: int, 
    tipo: str
) -> Optional[ImagenAgente]:
    """Actualiza los datos de una imagen de agente"""
    db_imagen = get_imagen_agente(db, imagen_id)
    if not db_imagen:
        return None
    
    db_imagen.tipo = tipo
    db.commit()
    db.refresh(db_imagen)
    return db_imagen

def delete_imagen_agente(db: Session, imagen_id: int) -> bool:
    """Elimina una imagen de agente"""
    db_imagen = get_imagen_agente(db, imagen_id)
    if not db_imagen:
        return False
    
    # Eliminar el archivo físico si es posible
    try:
        file_path = os.path.join(os.getcwd(), db_imagen.url.lstrip('/'))
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        # Si no se puede eliminar el archivo, continuamos de todas formas
        pass
    
    db.delete(db_imagen)
    db.commit()
    return True