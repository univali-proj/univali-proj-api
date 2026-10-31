import importlib
import pkgutil

from fastapi import APIRouter, FastAPI


def build_router() -> APIRouter:
    """Agrega automaticamente todo módulo de `app.router` que exponha um `router: APIRouter`."""
    api_router = APIRouter()

    for module_info in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
        if module_info.name.startswith("_"):
            continue

        module = importlib.import_module(f"{__name__}.{module_info.name}")
        router = getattr(module, "router", None)
        if isinstance(router, APIRouter):
            api_router.include_router(router)

    return api_router


def register_routers(app: FastAPI, prefix: str = "") -> None:
    app.include_router(build_router(), prefix=prefix)