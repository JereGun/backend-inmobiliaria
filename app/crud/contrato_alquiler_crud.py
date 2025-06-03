from sqlalchemy.orm import Session
from app.models.contrato_alquiler import ContratoAlquiler
from app.schemas.contrato_alquiler import ContratoAlquilerCreate, ContratoAlquilerUpdate
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta # For adding months easily
from sqlalchemy import func # Added func

def calculate_next_increase_date(start_date: date, interval_months: int) -> date:
    return start_date + relativedelta(months=interval_months)

def get_contrato_alquiler(db: Session, contrato_id: int) -> ContratoAlquiler | None:
    return db.query(ContratoAlquiler).filter(ContratoAlquiler.id == contrato_id).first()

def get_contratos_alquiler_by_propiedad(db: Session, propiedad_id: int, skip: int = 0, limit: int = 100) -> list[ContratoAlquiler]:
    return db.query(ContratoAlquiler).filter(ContratoAlquiler.propiedad_id == propiedad_id).offset(skip).limit(limit).all()

def get_contratos_alquiler_by_inquilino(db: Session, inquilino_id: int, skip: int = 0, limit: int = 100) -> list[ContratoAlquiler]:
    return db.query(ContratoAlquiler).filter(ContratoAlquiler.inquilino_id == inquilino_id).offset(skip).limit(limit).all()

def get_all_contratos_alquiler(db: Session, skip: int = 0, limit: int = 100) -> list[ContratoAlquiler]:
    return db.query(ContratoAlquiler).offset(skip).limit(limit).all()

def create_contrato_alquiler(db: Session, contrato: ContratoAlquilerCreate) -> ContratoAlquiler:
    # Ensure fecha_proximo_aumento is correctly set if not provided directly or calculated from fecha_inicio
    if not contrato.fecha_proximo_aumento:
         contrato.fecha_proximo_aumento = calculate_next_increase_date(contrato.fecha_inicio, contrato.intervalo_aumento_meses)

    db_contrato = ContratoAlquiler(**contrato.model_dump())
    db.add(db_contrato)
    db.commit()
    db.refresh(db_contrato)
    return db_contrato

def update_contrato_alquiler(db: Session, contrato_id: int, contrato_update_data: ContratoAlquilerUpdate) -> ContratoAlquiler | None:
    db_contrato = get_contrato_alquiler(db, contrato_id)
    if not db_contrato:
        return None

    update_data = contrato_update_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_contrato, key, value)

    # If the rent amount is updated, and there's an increase interval,
    # recalculate the next increase date from the *current date* or a specified 'last increase date'.
    # For simplicity, if monto_alquiler_actual is changed, we assume the increase just happened.
    # The notification should have been for 'fecha_proximo_aumento'.
    # So, the *new* 'fecha_proximo_aumento' is 'fecha_proximo_aumento' + interval.
    if 'monto_alquiler_actual' in update_data and db_contrato.intervalo_aumento_meses > 0:
        # The user is confirming the new rent for the period starting 'fecha_proximo_aumento'
        # So, the *next* increase will be 'intervalo_aumento_meses' from the *current* 'fecha_proximo_aumento'
         db_contrato.fecha_proximo_aumento = calculate_next_increase_date(db_contrato.fecha_proximo_aumento, db_contrato.intervalo_aumento_meses)


    db.add(db_contrato)
    db.commit()
    db.refresh(db_contrato)
    return db_contrato

def get_contratos_pendientes_notificacion_aumento(db: Session, notification_days_before: int = 30) -> list[ContratoAlquiler]:
    # TODO: Implement a background task (e.g., Celery) that periodically calls this function
    # to find contracts needing rent increase notifications.
    # The task would then iterate through the results and send notifications (e.g., email, in-app).
    # After a notification is successfully sent for a contract's specific 'fecha_proximo_aumento',
    # 'fecha_ultima_notificacion_aumento' should be updated to prevent re-notification for the same event.
    '''
    Gets contracts where the next rent increase date is within 'notification_days_before'
    and no notification has been sent after the previous increase period.
    '''
    today = date.today()
    notification_window_start = today
    notification_window_end = today + timedelta(days=notification_days_before)

    query = db.query(ContratoAlquiler).filter(
        ContratoAlquiler.fecha_proximo_aumento >= notification_window_start,
        ContratoAlquiler.fecha_proximo_aumento <= notification_window_end,
        ContratoAlquiler.estado == 'VIGENTE' # Assuming EstadoContratoEnum.VIGENTE.value
    )
    # This condition ensures we don't send multiple notifications for the same upcoming increase.
    # It checks if a notification was already sent *after* the *previous* increase date.
    # The previous increase date would be 'fecha_proximo_aumento' - 'intervalo_aumento_meses'.
    # This part can be tricky and might need adjustment based on exact notification flow.
    # For now, we'll assume 'fecha_ultima_notificacion_aumento' is cleared or set to null
    # when a rent amount is updated by the user, signifying the increase was handled.
    # Or, it's set when a notification is sent.
    # A simpler rule: notify if 'fecha_ultima_notificacion_aumento' is None or older than (fecha_proximo_aumento - interval).
    # query = query.filter(
    #     (ContratoAlquiler.fecha_ultima_notificacion_aumento == None) |
    #     (ContratoAlquiler.fecha_ultima_notificacion_aumento < (ContratoAlquiler.fecha_proximo_aumento - timedelta(days=ContratoAlquiler.intervalo_aumento_meses * 30))) # Approximate
    # )
    # A more robust way: The notification system should set 'fecha_ultima_notificacion_aumento'.
    # When the user updates the rent, 'fecha_proximo_aumento' is updated.
    # We notify if current date is between (old 'fecha_proximo_aumento' - notification_window) and (old 'fecha_proximo_aumento')
    # AND 'fecha_ultima_notificacion_aumento' is before (old 'fecha_proximo_aumento' - interval).
    # For now, let's keep it simple: notify if it's in window and not recently notified.
    # This assumes 'fecha_ultima_notificacion_aumento' is updated upon sending a notification.
    # If 'fecha_ultima_notificacion_aumento' is null, it means either it's a new contract or notification was never sent for current cycle.
    query = query.filter(
        (ContratoAlquiler.fecha_ultima_notificacion_aumento == None) |
        (ContratoAlquiler.fecha_ultima_notificacion_aumento < func.date(ContratoAlquiler.fecha_proximo_aumento, '-1 day')) # Ensure notification was before the due date
    )


    return query.all()

# Placeholder for delete if necessary, but usually contracts are archived or their state is changed.
# def delete_contrato_alquiler(db: Session, contrato_id: int):
#     db_contrato = get_contrato_alquiler(db, contrato_id)
#     if db_contrato:
#         db.delete(db_contrato)
#         db.commit()
#     return db_contrato
