from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.orm import joinedload
from app.models.direccion import Provincia, Localidad
import app.schemas.direccion as schemas
import app.models.direccion as models
from app.core.database import get_db

router = APIRouter(
    prefix="/direccion",
    tags=["Dirección"]
)

# TODO Pais-Routers
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

@router.put("/pais/{pais_id}", response_model=schemas.PaisOut, response_model_exclude_unset=True)
def actualizar_pais(pais_id: int, pais:schemas.PaisCreate, db: Session = Depends(get_db)):
    db_pais = db.query(models.Pais).filter(models.Pais.id == pais_id).first()
    if not db_pais:
        raise HTTPException(status_code=404, detail="País no encontrado")
    
    for key, value in pais.model_dump().items():
        setattr(db_pais, key, value)
    
    db.commit()
    db.refresh(db_pais)
    return db_pais

@router.delete("/pais/{pais_id}", status_code=204)
def eliminar_pais(pais_id: int, db: Session = Depends(get_db)):
    db_pais = db.query(models.Pais).filter(models.Pais.id == pais_id).first()
    if not db_pais:
        raise HTTPException(status_code=404, detail="País no encontrado")
    
    db.delete(db_pais)
    db.commit()
    return None

# TODO Provincia-Routers
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

@router.put("/provincia/{provincia_id}", response_model=schemas.ProvinciaOut, response_model_exclude_unset=True)
def actualizar_provincia(provincia_id: int, provincia: schemas.ProvinciaCreate, db: Session = Depends(get_db)):
    db_provincia = db.query(models.Provincia).filter(models.Provincia.id == provincia_id).first()
    if not db_provincia:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    
    # Verificar si el país existe
    pais = db.query(models.Pais).filter(models.Pais.id == provincia.pais_id).first()
    if not pais:
        raise HTTPException(status_code=404, detail="País no encontrado")
    
    for key, value in provincia.model_dump().items():
        setattr(db_provincia, key, value)

    db.commit()
    db.refresh(db_provincia)
    return db_provincia

@router.delete("/provincia/{provincia_id}", status_code=204)
def eliminar_provincia(provincia_id: int, db: Session = Depends(get_db)):
    db_provincia = db.query(models.Provincia).filter(models.Provincia.id == provincia_id).first()
    if not db_provincia:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    db.delete(db_provincia)
    db.commit()
    return None

# TODO Localidad-Routers
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
    localidades = db.query(Localidad).options(joinedload(Localidad.provincia)).all()
    return localidades

@router.put("/localidad/{localidad_id}", response_model=schemas.LocalidadOut, response_model_exclude_unset=True)
def actualizar_localidad(localidad_id: int, localidad: schemas.LocalidadCreate, db: Session = Depends(get_db)):
    db_localidad = db.query(models.Localidad).filter(models.Localidad.id == localidad_id).first()
    
    if not db_localidad:
        raise HTTPException(status_code=404, detail="Localidad no encontrada")
    
    # Verificar si la provincia asociada existe
    if not db.query(models.Provincia).filter(models.Provincia.id == localidad.provincia_id).first():
        raise HTTPException(status_code=400, detail="La provincia especificada no existe")
    
    for key, value in localidad.model_dump().items():
        setattr(db_localidad, key, value)

    db.commit()
    db.refresh(db_localidad)
    return db_localidad

@router.delete("/localidad/{localidad_id}", status_code=204)
def eliminar_localidad(localidad_id: int, db: Session = Depends(get_db)):
    db_localidad = db.query(models.Localidad).filter(models.Localidad.id == localidad_id).first()
    if not db_localidad:
        raise HTTPException(status_code=404, detail="Localidad no encontrada")
    db.delete(db_localidad)
    db.commit()
    return None

# TODO: Direccion-Routers
@router.post("/direccion", response_model=schemas.DireccionOut, response_model_exclude_unset=True)
def crear_direccion(direccion: schemas.DireccionCreate, db: Session = Depends(get_db)):
    # Verificar si la localidad existe
    localidad = db.query(models.Localidad).filter(models.Localidad.id == direccion.localidad_id).first()
    if not localidad:
        raise HTTPException(status_code=404, detail="Localidad no encontrada")
    
    # Verificar si la provincia existe
    provincia = db.query(models.Provincia).filter(models.Provincia.id == direccion.provincia_id).first()
    if not provincia:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    
    # Verificar si el país existe
    pais = db.query(models.Pais).filter(models.Pais.id == direccion.pais_id).first()
    if not pais:
        raise HTTPException(status_code=404, detail="País no encontrado")
    
    db_direccion = models.Direccion(**direccion.model_dump())
    db.add(db_direccion)
    db.commit()
    db.refresh(db_direccion)
    return db_direccion

@router.get("/direcciones", response_model=List[schemas.DireccionOut])
def obtener_direcciones(db: Session = Depends(get_db)):
    direcciones = db.query(models.Direccion).options(joinedload(models.Direccion.localidad)).all()
    return direcciones

@router.put("/direccion/{direccion_id}", response_model=schemas.DireccionOut, response_model_exclude_unset=True)
def actualizar_direccion(direccion_id: int, direccion: schemas.DireccionCreate, db: Session = Depends(get_db)):
    db_direccion = db.query(models.Direccion).filter(models.Direccion.id == direccion_id).first()
    if not db_direccion:
        raise HTTPException(status_code=404, detail="Localidad no encontrada")
    for key, value in direccion.model_dump().items():
        setattr(db_direccion, key, value)

    db.commit()
    db.refresh(db_direccion)
    return db_direccion

@router.delete("/direccion/{direccion_id}", status_code=204)
def eliminar_direccion(direccion_id: int, db: Session = Depends(get_db)):
    db_direccion = db.query(models.Direccion).filter(models.Direccion.id == direccion_id).first()
    if not db_direccion:
        raise HTTPException(status_code=404, detail="Direccion no encontrada")
    db.delete(db_direccion)
    db.commit()
    return None