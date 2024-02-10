import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.api.v1.api import api_router
from src.core.config import get_settings
from src.utils.logger import init_loguru_logger


def configure_app() -> FastAPI:
    setting = get_settings()
    origins = ["*"]

    app = FastAPI(
        title=setting.core.project_name,
        openapi_url=f"{setting.core.api_str}/openapi.json",
        debug=setting.core.debug,
    )
    app.add_middleware(SessionMiddleware, secret_key=setting.core.secret_key)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix=setting.core.api_str)

    init_loguru_logger(app)

    return app


def main() -> None:
    setting = get_settings()
    uvicorn.run(
        "main:configure_app",
        port=8000,
        reload=setting.core.debug,
        factory=True,
    )


if __name__ == "__main__":
    main()
