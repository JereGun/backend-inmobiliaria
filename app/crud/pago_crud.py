from sqlalchemy.orm import Session
from app.models.pago import Pago
from app.models.factura import Factura
from app.schemas.pago import PagoCreate
from app.crud.factura_crud import get_factura, update_factura_estado_pago
from app.models.enums import EstadoPagoFacturaEnum
from decimal import Decimal

def get_pago(db: Session, pago_id: int) -> Pago | None:
    return db.query(Pago).filter(Pago.id == pago_id).first()

def get_pagos_by_factura(db: Session, factura_id: int, skip: int = 0, limit: int = 100) -> list[Pago]:
    return db.query(Pago).filter(Pago.factura_id == factura_id).order_by(Pago.fecha_pago.desc()).offset(skip).limit(limit).all()

def create_pago(db: Session, pago_in: PagoCreate) -> tuple[Pago | None, str | None]:
    db_factura = get_factura(db, pago_in.factura_id)
    if not db_factura:
        return None, "Factura no encontrada."

    current_factura_estado = db_factura.estado_pago
    # Ensure comparison is with Enum member if current_factura_estado is string from DB
    if not isinstance(current_factura_estado, EstadoPagoFacturaEnum):
        try:
            current_factura_estado = EstadoPagoFacturaEnum(str(current_factura_estado))
        except ValueError:
             # Handle case where string value from DB isn't a valid enum member
             return None, f"Estado de factura desconocido: {current_factura_estado}"


    if current_factura_estado == EstadoPagoFacturaEnum.ANULADA:
        return None, "No se pueden aplicar pagos a una factura anulada."

    if current_factura_estado == EstadoPagoFacturaEnum.PAGADA and db_factura.monto_adeudado <= Decimal("0.00"):
        return None, "La factura ya está completamente pagada."

    db_pago = Pago(**pago_in.model_dump())
    db.add(db_pago)
    # We commit here to get db_pago.id, but this means if update_factura_estado_pago fails,
    # the pago is still committed. A more robust transaction would wrap both.
    # However, update_factura_estado_pago also commits.
    # For simplicity now, we commit pago first.
    db.commit()
    db.refresh(db_pago)

    # Recalculate total_pagado on the factura after this new pago
    # It's important to refresh db_factura to ensure its 'pagos' collection is up-to-date
    # if the session used by get_factura is different or if 'pagos' relationship is not eagerly loaded.
    # However, since update_factura_estado_pago re-fetches the factura, this should be fine.

    # Calculate new monto_adeudado
    # Sum all 'monto_pagado' for this factura_id from the 'pagos' table
    # This is more reliable than db_factura.pagos if the collection isn't perfectly synced
    # or if there are concurrent payments (though less likely in typical web request).

    # Re-fetch factura to ensure its 'pagos' relationship is fresh for sum()
    # This is important because db_factura might be stale after db_pago commit.
    db.refresh(db_factura) # Refresh to get the latest state of the factura object itself.
                           # However, for relationships like 'pagos', they might need explicit refresh
                           # or re-fetching if not properly configured for eager loading / session management.
                           # A simpler way for 'total_pagado_actual' is to query sum from Pago table.

    # Let's sum directly from the Pago table for accuracy after commit
    total_pagado_query = db.query(Session.query(Pago.monto_pagado).filter(Pago.factura_id == pago_in.factura_id).sum())
    scalar_total_pagado = total_pagado_query.scalar() or Decimal("0.00")

    nuevo_monto_adeudado = db_factura.monto_total - scalar_total_pagado

    updated_factura = update_factura_estado_pago(db=db, factura_id=db_factura.id, nuevo_monto_adeudado=nuevo_monto_adeudado)

    if not updated_factura:
        # This case should ideally not happen if db_factura was found.
        # Consider how to handle; maybe roll back db_pago if critical.
        return db_pago, "Pago registrado, pero hubo un error actualizando el estado de la factura."

    return db_pago, None
