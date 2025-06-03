from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.contrato_alquiler import ContratoAlquiler, ContratoAlquilerCreate, ContratoAlquilerUpdate
from app.crud import contrato_alquiler_crud as crud
from app.models.enums import EstadoContratoEnum # For query param validation

router = APIRouter()

@router.post("/", response_model=ContratoAlquiler, status_code=201)
def create_contrato_alquiler(
    contrato_in: ContratoAlquilerCreate,
    db: Session = Depends(get_db)
):
    # Additional validation can be added here, e.g., check if property or inquilino exist
    return crud.create_contrato_alquiler(db=db, contrato=contrato_in)

@router.get("/{contrato_id}", response_model=ContratoAlquiler)
def read_contrato_alquiler(
    contrato_id: int,
    db: Session = Depends(get_db)
):
    db_contrato = crud.get_contrato_alquiler(db, contrato_id=contrato_id)
    if db_contrato is None:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")
    return db_contrato

@router.put("/{contrato_id}", response_model=ContratoAlquiler)
def update_contrato_alquiler(
    contrato_id: int,
    contrato_in: ContratoAlquilerUpdate,
    db: Session = Depends(get_db)
):
    db_contrato = crud.get_contrato_alquiler(db, contrato_id=contrato_id)
    if db_contrato is None:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")

    # The user updates the rent amount here.
    # The CRUD operation handles recalculating fecha_proximo_aumento.
    updated_contrato = crud.update_contrato_alquiler(db=db, contrato_id=contrato_id, contrato_update_data=contrato_in)
    return updated_contrato

@router.get("/propiedad/{propiedad_id}", response_model=List[ContratoAlquiler])
def read_contratos_by_propiedad(
    propiedad_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(default=100, ge=1, le=200)
):
    contratos = crud.get_contratos_alquiler_by_propiedad(db, propiedad_id=propiedad_id, skip=skip, limit=limit)
    return contratos

@router.get("/inquilino/{inquilino_id}", response_model=List[ContratoAlquiler])
def read_contratos_by_inquilino(
    inquilino_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(default=100, ge=1, le=200)
):
    contratos = crud.get_contratos_alquiler_by_inquilino(db, inquilino_id=inquilino_id, skip=skip, limit=limit)
    return contratos

@router.get("/", response_model=List[ContratoAlquiler])
def read_all_contratos(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(default=100, ge=1, le=200),
    estado: Optional[EstadoContratoEnum] = None # Allow filtering by state
):
    # This endpoint might need more sophisticated filtering in a real app
    # For now, it's a simple retrieval, potentially filtered by state
    # The crud.get_all_contratos_alquiler would need to be modified to support filtering
    # For now, let's assume we fetch all and filter in code if 'estado' is provided (not ideal for performance)
    # Or, modify the crud function if time permits.
    # For simplicity, this example doesn't implement filtering in the CRUD for get_all.
    # A more robust version would pass the filter to the CRUD layer.
    contratos = crud.get_all_contratos_alquiler(db, skip=skip, limit=limit)
    if estado:
        contratos = [c for c in contratos if c.estado == estado]
    return contratos

# Endpoint for fetching contracts pending notification - useful for admin or automated tasks
@router.get("/pendientes-notificacion/", response_model=List[ContratoAlquiler])
def get_contratos_pendientes_notificacion(
    notification_days_before: int = Query(default=30, ge=1, le=90),
    db: Session = Depends(get_db)
):
    contratos = crud.get_contratos_pendientes_notificacion_aumento(db, notification_days_before=notification_days_before)
    return contratos
