from app.router import build_router
from fastapi import APIRouter, FastAPI

app = APIRouter(prefix="/test", tags=["Test"])

# Endpoint simples para validar a comunicação com o frontend.
@app.get("", response_class=PlainTextResponse, tags=["Health"])
async def test_endpoint() -> str:
    return "hello world"