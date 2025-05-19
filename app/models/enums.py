import enum
from sqlalchemy.dialects.postgresql import ENUM

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