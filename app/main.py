from fastapi import FastAPI
from app.config import tags_metadata
from app.routers import direccion

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

app.include_router(direccion.router)