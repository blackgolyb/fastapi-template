from fastapi import APIRouter, Request
from loguru import logger

router = APIRouter()


@router.get("/")
def index(request: Request) -> dict[str, str]:
    logger.info("PONG")
    return {"ping": "pong!"}
