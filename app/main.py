from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import tags_metadata
from app.api.v1.routes import direccion
from app.api.v1.routes import cliente
from app.api.v1.routes import agente

app = FastAPI(
    title="API de Gestion Inmobiliaria",
    description="Esta API permite gestionar una inmobiliaria",
    version="1.0.0",
    contact={
        "name": "Gunsett Jeremias",
        "email": "jere.gunsett@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/doc",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=tags_metadata
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(direccion.router)
app.include_router(cliente.router)
app.include_router(agente.router)