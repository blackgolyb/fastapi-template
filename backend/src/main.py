import uvicorn
from fastapi import APIRouter, FastAPI, Request
from loguru import logger
from utils.logger import init_logger

main_router = APIRouter()


@main_router.get("/")
def index(request: Request) -> dict[str, str]:
    logger.info("PONG")
    return {"ping": "pong!"}


def main() -> None:
    app = FastAPI(title="Test Uvicorn Handlers")
    app.include_router(main_router)

    init_logger(app)

    uvicorn.run(app, port=8009)


if __name__ == "__main__":
    main()
