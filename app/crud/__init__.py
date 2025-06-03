from .contrato_alquiler_crud import (
    create_contrato_alquiler,
    get_contrato_alquiler,
    get_contratos_alquiler_by_propiedad,
    get_contratos_alquiler_by_inquilino,
    get_all_contratos_alquiler,
    update_contrato_alquiler,
    get_contratos_pendientes_notificacion_aumento
)
# Import modules, some aliased for consistency or convenience
from . import imagen_crud as imagenes
from . import factura_crud
from . import pago_crud
from . import propiedad_crud # Added as per plan

# It's generally better to expose specific functions if that's the desired interface,
# or consistently expose modules. The current __all__ is mixed.
# For now, adding new crud modules to __all__.
# And keeping existing function exports from contrato_alquiler_crud.

__all__ = [
    # Functions from contrato_alquiler_crud
    "create_contrato_alquiler",
    "get_contrato_alquiler",
    "get_contratos_alquiler_by_propiedad",
    "get_contratos_alquiler_by_inquilino",
    "get_all_contratos_alquiler",
    "update_contrato_alquiler",
    "get_contratos_pendientes_notificacion_aumento",
    # Modules
    "imagenes",
    "factura_crud",
    "pago_crud",
    "propiedad_crud",
]
