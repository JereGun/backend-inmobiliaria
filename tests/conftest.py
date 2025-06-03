import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SQLAlchemySession # Renamed to avoid conflict
from app.main import app
from app.core.database import Base, get_db
import os

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URL = os.environ.get("TEST_DATABASE_URL", "sqlite:///./test.db")


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables once for the test session
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db() -> SQLAlchemySession: # Use SQLAlchemySession for type hint
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Begin a nested transaction (optional, depends on specific needs)
    # nested = session.begin_nested()

    # @session.event.listens_for(session, "after_transaction_end")
    # def end_savepoint(session, transaction):
    #     if not nested.is_active:
    #         session.begin_nested()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="function")
def client(db: SQLAlchemySession) -> TestClient: # client uses the db fixture
    def override_get_db_for_test():
        try:
            yield db
        finally:
            pass # The db fixture handles closing

    app.dependency_overrides[get_db] = override_get_db_for_test
    yield TestClient(app)
    del app.dependency_overrides[get_db] # Clean up override

# --- Add simplified prerequisite data fixtures below ---
# These should ideally be in their own files or a more organized structure
# For now, keeping them here for simplicity as reported by the previous subtask.

from app.models import Pais, Provincia, Localidad, Direccion, Cliente, Propiedad
from app.models.enums import TipoDocumentoEnum, GeneroEnum, SituacionFiscalEnum, TipoPropeidadEnum, TipoOperacionEnum, EstadoEnum
from datetime import date # Already imported at top, but good for clarity here

@pytest.fixture(scope="function")
def test_pais(db: SQLAlchemySession) -> Pais:
    pais = Pais(nombre="Argentina")
    db.add(pais)
    db.commit()
    db.refresh(pais)
    return pais

@pytest.fixture(scope="function")
def test_provincia(db: SQLAlchemySession, test_pais: Pais) -> Provincia:
    provincia = Provincia(nombre="Buenos Aires", pais_id=test_pais.id)
    db.add(provincia)
    db.commit()
    db.refresh(provincia)
    return provincia

@pytest.fixture(scope="function")
def test_localidad(db: SQLAlchemySession, test_provincia: Provincia) -> Localidad:
    localidad = Localidad(nombre="La Plata", provincia_id=test_provincia.id) # Removed codigo_postal
    db.add(localidad)
    db.commit()
    db.refresh(localidad)
    return localidad

@pytest.fixture(scope="function")
def test_direccion(db: SQLAlchemySession, test_localidad: Localidad) -> Direccion:
    direccion = Direccion(
        calle="Calle Falsa",
        altura=123, # Corrected from 'numero'
        piso="PB",
        dpto="A",
        localidad_id=test_localidad.id,
        # These were missing in the original Direccion model, but good to have for completeness if model supports
        pais_id=test_localidad.provincia.pais_id,
        provincia_id=test_localidad.provincia_id,
        codigo_postal="1900" # Set directly
    )
    db.add(direccion)
    db.commit()
    db.refresh(direccion)
    return direccion

@pytest.fixture(scope="function")
def test_inquilino(db: SQLAlchemySession, test_direccion: Direccion) -> Cliente:
    inquilino = Cliente(
        nombre="Test Inquilino",
        apellido="Uno",
        tipo_documento=TipoDocumentoEnum.DNI,
        numero_documento="12345678",
        email="inquilino@example.com",
        # Assuming Cliente model has direccion_id and other necessary fields
        # If not, these need to be adjusted to what Cliente model expects
        direccion_id=test_direccion.id,
        telefono="1122334455",
        genero=GeneroEnum.OTRO, # Assuming GeneroEnum.OTRO exists
        fecha_nacimiento=date(1990,1,1),
        situacion_fiscal=SituacionFiscalEnum.CONSUMIDOR_FINAL # Assuming this enum and value exist
    )
    db.add(inquilino)
    db.commit()
    db.refresh(inquilino)
    return inquilino

@pytest.fixture(scope="function")
def test_propiedad(db: SQLAlchemySession, test_direccion: Direccion, test_inquilino: Cliente) -> Propiedad:
    propiedad = Propiedad(
        nombre="Casa de Test", # Was 'titulo'
        direccion_id=test_direccion.id,
        tipo_propiedad=TipoPropeidadEnum.casa, # was .departamento
        tipo_operacion=TipoOperacionEnum.alquiler,
        propietario_id=test_inquilino.id, # Using inquilino as propietario for simplicity
        estado=EstadoEnum.activo,
        precio_alquiler=50000,
        # Adjusted characteristic fields based on Propiedad model from previous logs
        ano_construccion=date.today().year - 5,
        banios=1,
        dormitorios=2,
        ambientes=3,
        cochera=1,
        superficie_cubierta=60,
        superficie_descubierta=10
        # 'descripcion' is also a field in Propiedad model, can be added if needed by tests
        # 'agente_id' is also a field, can be added if needed
    )
    db.add(propiedad)
    db.commit()
    db.refresh(propiedad)
    return propiedad
