from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.models.agente as models
import app.schemas.agente as schemas
from app.core.database import get_db

router = APIRouter(
    prefix="/agente",
    tags=["Agente"]
)

# TODO Agente-Routers
@router.post("/agente", response_model=schemas.AgenteOut, response_model_exclude_unset=True)
def crear_agente(agente: schemas.AgenteCreate, db: Session = Depends(get_db)):
    db_agente = models.Agente(**agente.model_dump())
    db.add(db_agente)
    db.commit()
    db.refresh(db_agente)
    return db_agente

@router.get("/agentes", response_model=List[schemas.AgenteOut], response_model_exclude_unset=True)
def obtener_agentes(db: Session = Depends(get_db)):
    return db.query(models.Agente).all()

@router.get("/agente/{agente_id}", response_model=schemas.AgenteOut, response_model_exclude_unset=True)
def obtener_agente(agente_id: int, db: Session = Depends(get_db)):
    db_agente = db.query(models.Agente).filter(models.Agente.id == agente_id).first()
    if not db_agente:
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    return db_agente

@router.put("/agente/{agente_id}", response_model=schemas.AgenteOut, response_model_exclude_unset=True)
def actualizar_agente(agente_id: int, agente: schemas.AgenteCreate, db: Session = Depends(get_db)):
    db_agente = db.query(models.Agente).filter(models.Agente.id == agente_id).first()
    if not db_agente:
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    
    for key, value in agente.model_dump().items():
        setattr(db_agente, key, value)
    
    db.commit()
    db.refresh(db_agente)
    return db_agente

@router.delete("/agente/{agente_id}", status_code=204)
def eliminar_agente(agente_id: int, db: Session = Depends(get_db)):
    db_agente = db.query(models.Agente).filter(models.Agente.id == agente_id).first()
    if not db_agente:
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    
    db.delete(db_agente)
    db.commit()
    return None

@router.get("/agente/activos", response_model=List[schemas.AgenteOut], response_model_exclude_unset=True)
def obtener_agentes_activos(db: Session = Depends(get_db)):
    return db.query(models.Agente).filter(models.Agente.activo is True).all()

