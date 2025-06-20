import enum
from sqlalchemy.dialects.postgresql import ENUM

# Enum para el cliente y agente
class TipoDocumentoEnum(str, enum.Enum):
    DNI = "DNI"
    CUIT = "CUIT"
    CUIL = "CUIL"
    PASAPORTE = "PASAPORTE"
    OTRO = "OTRO"

tipo_documento_enum = ENUM (
    TipoDocumentoEnum,
    name="tipo_documento_enum",
    create_type=False
)

class GeneroEnum(str, enum.Enum):
    MASCULINO = "MASCULINO"
    FEMENINO = "FEMENINO"
    OTRO = "OTRO"

genero_enum = ENUM (
    GeneroEnum,
    name="genero_enum",
    create_type=False
)

class SituacionFiscalEnum(str, enum.Enum):
    RESPONSABLE_INSCRIPTO = "RESPONSABLE_INSCRIPTO"
    RESPONSABLE_NO_INSCRIPTO = "RESPONSABLE_NO_INSCRIPTO"
    EXENTO = "EXENTO"
    CONSUMIDOR_FINAL = "CONSUMIDOR_FINAL"
    MONOTRIBUTO = "MONOTRIBUTO"
    NO_RESPONSABLE = "NO_RESPONSABLE"
    OTRO = "OTRO"

situacion_fiscal_enum = ENUM (
    SituacionFiscalEnum,
    name="situacion_fiscal_enum",
    create_type=False
)

# Enum para la propiedad
class TipoPropeidadEnum(str, enum.Enum):
    casa = "Casa"
    departamento = "Departamento"
    oficina = "Oficina"
    local_comercial = "Local Comercial"
    terreno = "Terreno"
    cochera = "Cochera"
    galpon = "Galpon"
    otro = "Otro"

tipo_propiedad_enum = ENUM (
    TipoPropeidadEnum,
    name="tipo_propiedad_enum",
    create_type=False
)

class TipoOperacionEnum(str, enum.Enum):
    venta = "Venta"
    alquiler = "Alquiler"
    ambos = "Ambos"

tipo_operacion_enum = ENUM (
    TipoOperacionEnum,
    name="tipo_operacion_enum",
    create_type=False
)

class EstadoEnum(str, enum.Enum):
    borrador = "Borrador"
    activo = "Activo"
    inactivo = "Inactivo"
    reservado = "Reservado"
    vendido = "Vendido"
    alquilado = "Alquilado"

estado_enum = ENUM (
    EstadoEnum,
    name="estado_enum",
    create_type=False
)