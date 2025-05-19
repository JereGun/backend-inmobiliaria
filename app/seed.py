from sqlalchemy.orm import Session
from datetime import date, datetime
from app.database import SessionLocal
from app.models.direccion.direccion_model import Direccion, Localidad, Provincia, Pais
from app.models.cliente.cliente_model import Cliente
from app.models.agente.agente_model import Agente

# Enums
from app.models.enums import tipo_documento_enum, genero_enum, situacion_fiscal_enum

def seed_data(db: Session):
    # Crear país
    argentina = Pais(nombre="Argentina")
    db.add(argentina)
    db.commit()
    db.refresh(argentina)

    # Crear provincia
    buenos_aires = Provincia(nombre="Buenos Aires", pais_id=argentina.id)
    db.add(buenos_aires)
    db.commit()
    db.refresh(buenos_aires)

    # Crear localidad
    lanus = Localidad(nombre="Lanús", provincia_id=buenos_aires.id)
    db.add(lanus)
    db.commit()
    db.refresh(lanus)

    # Crear dirección
    direccion_1 = Direccion(
        calle="Av. Hipólito Yrigoyen",
        altura=1234,
        piso="1",
        dpto="A",
        entre_calles="25 de Mayo y Belgrano",
        observaciones="Frente a la plaza",
        codigo_postal=1824,
        barrio="Centro",
        localidad_id=lanus.id,
        provincia_id=buenos_aires.id,
        pais_id=argentina.id
    )
    db.add(direccion_1)
    db.commit()
    db.refresh(direccion_1)

    # Crear cliente
    cliente_1 = Cliente(
        nombre="Lucía",
        apellido="González",
        tipo_documento="DNI",
        numero_documento="30111222",
        email="lucia.gonzalez@example.com",
        telefono="1122334455",
        celular="1199887766",
        fecha_nacimiento=date(1990, 4, 15),
        genero="FEMENINO",
        situacion_fiscal="MONOTRIBUTO",
        direccion_id=direccion_1.id
    )
    db.add(cliente_1)

    # Crear agente
    agente_1 = Agente(
        nombre="Carlos",
        apellido="Pérez",
        tipo_documento="DNI",
        numero_documento="27123456",
        telefono="1133445566",
        email="carlos.perez@example.com",
        fecha_nacimiento=datetime(1985, 6, 20),
        activo=True,
        licencia="AG123456",
        fecha_alta=datetime.utcnow(),
        direccion_id=direccion_1.id
    )
    db.add(agente_1)

    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    seed_data(db)
    db.close()