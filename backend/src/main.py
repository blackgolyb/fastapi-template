import uvicorn
from fastapi import FastAPI
from utils.logger import init_logger

from src.api.v1.api import api_router


def main() -> None:
    app = FastAPI(title="Test Uvicorn Handlers")
    app.include_router(api_router)

    init_logger(app)

    uvicorn.run(app, port=8009)


if __name__ == "__main__":
    main()
