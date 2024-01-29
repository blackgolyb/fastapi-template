import uvicorn
from fastapi import FastAPI

from src.api.v1.api import api_router
from src.core.config import get_settings
from src.utils.logger import init_loguru_logger


def configure_app() -> FastAPI:
    setting = get_settings()

    app = FastAPI(title=setting.core.project_name, debug=setting.core.debug)
    app.include_router(api_router)

    init_loguru_logger(app)

    return app


def main() -> None:
    setting = get_settings()
    uvicorn.run(
        "main:configure_app",
        port=8009,
        reload=setting.core.debug,
        factory=True,
    )


if __name__ == "__main__":
    main()
