import importlib
import pkgutil

from app.core.database import Base

# Importa todos os módulos do pacote para registrar os modelos em Base.metadata
for _module_info in pkgutil.iter_modules(__path__):
    if not _module_info.name.startswith("_"):
        importlib.import_module(f"{__name__}.{_module_info.name}")

__all__ = ["Base"]