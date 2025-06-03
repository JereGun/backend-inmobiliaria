from sqlalchemy.orm import Session
from app.models.factura import Factura
from app.schemas.factura import FacturaCreate, FacturaUpdate
from app.models.enums import EstadoPagoFacturaEnum
from decimal import Decimal

def get_factura(db: Session, factura_id: int) -> Factura | None:
    return db.query(Factura).filter(Factura.id == factura_id).first()

def get_facturas_by_cliente(db: Session, cliente_id: int, skip: int = 0, limit: int = 100) -> list[Factura]:
    return db.query(Factura).filter(Factura.cliente_id == cliente_id).order_by(Factura.fecha_emision.desc()).offset(skip).limit(limit).all()

def get_all_facturas(db: Session, skip: int = 0, limit: int = 100) -> list[Factura]:
    return db.query(Factura).order_by(Factura.fecha_emision.desc()).offset(skip).limit(limit).all()

def create_factura(db: Session, factura_in: FacturaCreate) -> Factura:
    calculated_total = factura_in.monto_base + factura_in.monto_iva
    if factura_in.monto_total != calculated_total:
        factura_in.monto_total = calculated_total

    current_estado_pago = factura_in.estado_pago
    if isinstance(current_estado_pago, str):
        current_estado_pago = EstadoPagoFacturaEnum(current_estado_pago)
    elif current_estado_pago is None:
        current_estado_pago = EstadoPagoFacturaEnum.PENDIENTE

    db_factura_data = factura_in.model_dump(exclude_unset=True)
    # Ensure 'estado_pago' in db_factura_data is the enum object if it came from factura_in
    # If factura_in.estado_pago was already an enum, this is fine.
    # If it was a string that got converted, we need to make sure the converted value is used.
    db_factura_data['estado_pago'] = current_estado_pago

    db_factura = Factura(
        **db_factura_data,
        monto_adeudado=factura_in.monto_total # On creation, amount due is full amount
    )

    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    return db_factura

def update_factura(db: Session, factura_id: int, factura_in: FacturaUpdate) -> Factura | None:
    db_factura = get_factura(db, factura_id)
    if not db_factura:
        return None

    update_data = factura_in.model_dump(exclude_unset=True)

    if 'monto_base' in update_data or 'monto_iva' in update_data:
        new_base = update_data.get('monto_base', db_factura.monto_base)
        new_iva = update_data.get('monto_iva', db_factura.monto_iva)
        new_total = new_base + new_iva
        update_data['monto_total'] = new_total

        # If the outstanding amount was the full original total, update it to the new total.
        # This avoids issues if the invoice was PENDIENTE and its total changes.
        # If there were partial payments, this logic might need to be more complex.
        if db_factura.monto_adeudado == db_factura.monto_total:
             update_data['monto_adeudado'] = new_total

    for key, value in update_data.items():
        if key == 'estado_pago' and isinstance(value, str):
            setattr(db_factura, key, EstadoPagoFacturaEnum(value))
        else:
            setattr(db_factura, key, value)

    # Ensure estado_pago is an enum object before checking its value
    current_estado = db_factura.estado_pago
    if not isinstance(current_estado, EstadoPagoFacturaEnum):
         current_estado = EstadoPagoFacturaEnum(str(current_estado))

    if current_estado == EstadoPagoFacturaEnum.ANULADA:
        db_factura.monto_adeudado = Decimal("0.00")

    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    return db_factura

def update_factura_estado_pago(db: Session, factura_id: int, nuevo_monto_adeudado: Decimal) -> Factura | None:
    """Helper function to update factura payment status; called by pago_crud."""
    db_factura = get_factura(db, factura_id)
    if not db_factura:
        return None

    db_factura.monto_adeudado = nuevo_monto_adeudado

    current_estado = db_factura.estado_pago
    if not isinstance(current_estado, EstadoPagoFacturaEnum):
        current_estado = EstadoPagoFacturaEnum(str(current_estado))

    # Only update status if not already ANULADA
    if current_estado != EstadoPagoFacturaEnum.ANULADA:
        if nuevo_monto_adeudado <= Decimal("0.00"):
            db_factura.estado_pago = EstadoPagoFacturaEnum.PAGADA
        elif nuevo_monto_adeudado < db_factura.monto_total:
            db_factura.estado_pago = EstadoPagoFacturaEnum.PAGADA_PARCIALMENTE
        # If nuevo_monto_adeudado >= db_factura.monto_total, it means it's PENDIENTE (or reverted from partial)
        # This also handles the case where a payment might be deleted or adjusted upwards.
        elif nuevo_monto_adeudado >= db_factura.monto_total:
            # Ensure monto_adeudado does not exceed monto_total unless it's a special case not handled here
            db_factura.monto_adeudado = db_factura.monto_total
            db_factura.estado_pago = EstadoPagoFacturaEnum.PENDIENTE

    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    return db_factura
