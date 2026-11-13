from fastapi import APIRouter, FastAPI

app = APIRouter()

# Endpoint simples para validar a comunicação com o frontend.
@app.get("/test", response_class=PlainTextResponse, tags=["Health"])
async def test_endpoint() -> str:
    return "hello world"