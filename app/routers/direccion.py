from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.orm import joinedload
from app.models.direccion.direccion_model import Provincia, Localidad
import app.schemas.direccion.direccion as schemas
import app.models.direccion.direccion_model as models
from app.database import get_db

router = APIRouter(
    prefix="/direccion",
    tags=["Dirección"]
)

# Pais
@router.post("/pais", response_model=schemas.PaisOut, response_model_exclude_unset=True)
def crear_pais(pais: schemas.PaisCreate, db: Session = Depends(get_db)):
    db_pais = models.Pais(**pais.model_dump())
    db.add(db_pais)
    db.commit()
    db.refresh(db_pais)
    return db_pais

@router.get("/paises", response_model=List[schemas.PaisOut])
def obtener_paises(db: Session = Depends(get_db)):
    return db.query(models.Pais).all()


# Provincia
@router.post("/provincia", response_model=schemas.ProvinciaOut, response_model_exclude_unset=True)
def crear_provincia(provincia: schemas.ProvinciaCreate, db: Session = Depends(get_db)):
    # Verificar si el país existe
    pais = db.query(models.Pais).filter(models.Pais.id == provincia.pais_id).first()
    if not pais:
        raise HTTPException(status_code=404, detail="País no encontrado")
    
    db_provincia = models.Provincia(**provincia.model_dump())
    db.add(db_provincia)
    db.commit()
    db.refresh(db_provincia)
    return db_provincia

@router.get("/provincias", response_model=List[schemas.ProvinciaOut])
def obtener_provincias(db: Session = Depends(get_db)):
    provincias = db.query(Provincia).options(joinedload(Provincia.pais)).all()
    return provincias

# Localidad
@router.post("/localidad/", response_model=schemas.LocalidadOut, response_model_exclude_unset=True)
def crear_localidad(localidad: schemas.LocalidadCreate, db: Session = Depends(get_db)):
    provincia = db.query(models.Provincia).filter(models.Provincia.id == localidad.provincia_id).first()
    if not provincia:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")

    db_localidad = models.Localidad(nombre=localidad.nombre, provincia_id=localidad.provincia_id)
    db.add(db_localidad)
    db.commit()
    db.refresh(db_localidad)
    return db_localidad

@router.get("/localidades/", response_model=List[schemas.LocalidadOut])
def obtener_localidades(db: Session = Depends(get_db)):
    localidades =db.query(Localidad).options(joinedload(Localidad.provincia)).all()
    return localidades