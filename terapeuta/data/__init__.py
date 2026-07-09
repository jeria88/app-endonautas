"""
Paquete de datos clínicos del módulo terapeuta.

Reemplaza al antiguo `constants.py` (dividido para que el catálogo expandido no
crezca sin control). Reexporta los nombres de uso común para compatibilidad.
"""
from .frameworks import (  # noqa: F401
    FRAMEWORKS_AND_TECHNIQUES,
    KEYWORD_TO_FRAMEWORKS,
    get_all_tecnicas,
    get_framework_to_tecnicas_map,
    get_tecnica_to_framework_map,
)
from .catalogo_otros import DIAGNOSIS_OTROS  # noqa: F401
from .patrones_mtc import (  # noqa: F401
    MARCO_MTC,
    PATRONES_MTC,
    PATRONES_MTC_BY_ID,
)
from .prompts import (  # noqa: F401
    SYSTEM_DIFERENCIACION,
    SYSTEM_PROPUESTA,
)
