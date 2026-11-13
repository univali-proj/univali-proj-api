from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="/test", tags=["Test"])


@router.get("", response_class=PlainTextResponse)
async def test_endpoint() -> str:
    """Endpoint simples para validar a comunicação com o frontend."""
    return "hello world"
