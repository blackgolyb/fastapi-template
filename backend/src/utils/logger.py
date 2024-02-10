"""Configure handlers and formats for application loggers."""
import logging
import sys
from pprint import pformat
from typing import Any, Optional

from fastapi import FastAPI

from src.utils.singleton import SingletonMeta

try:
    from loguru import logger as _loguru_logger
    from loguru._defaults import LOGURU_FORMAT
except ImportError:
    ...


class Logger(metaclass=SingletonMeta):
    def __init__(self, logger: Optional[Any] = None) -> None:
        if logger is None:
            logger = logging.getLogger("uvicorn")

        self.logger = logger

    def __getattr__(self, __name: str, /) -> Any:
        if hasattr(self.logger, __name):
            return getattr(self.logger, __name)

        raise AttributeError(__name)


logger = Logger()


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentaion.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        level: str | int
        try:
            level = _loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back  # type: ignore
            depth += 1

        _loguru_logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def format_record(record: dict) -> str:
    """
    Custom format for loguru loggers.
    Uses pformat for log any data like request/response body during debug.
    Works with logging if loguru handler it.
    Example:
    >>> payload = [{"users":[{"name": "Nick", "age": 87, "is_active": True}, {"name": "Alex", "age": 27, "is_active": True}], "count": 2}]
    >>> logger.bind(payload=).debug("users payload")
    >>> [ { 'count': 2,
    >>>     'users': [ {'age': 87, 'is_active': True, 'name': 'Nick'},
    >>>                {'age': 27, 'is_active': True, 'name': 'Alex'}]}]
    """

    format_string = LOGURU_FORMAT

    if "payload" in record["extra"]:
        depth = record["extra"].get("payload-depth")
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=2, compact=True, width=88, depth=depth
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


def get_loggers_by_names(names: list[str]) -> list[logging.Logger]:
    """
    Get list of loggers by names.
    """
    return [logging.getLogger(name) for name in names]


def replace_logging_to_loguru(
    loggers_names: Optional[list[str]] = None,
    overwrite_loggers_names: Optional[list[str]] = None,
) -> None:
    """
    Replaces logging handlers with a handler for using the custom handler.

    WARNING!
    if you call the init_logging in startup event function,
    then the first logs before the application start will be in the old format
    >>> app.add_event_handler("startup", init_logging)
    stdout:
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [11528] using statreload
    INFO:     Started server process [6036]
    INFO:     Waiting for application startup.
    2020-07-25 02:19:21.357 | INFO     | uvicorn.lifespan.on:startup:34 - Application startup complete.
    """

    # disable handlers for specific uvicorn loggers
    # to redirect their output to the default uvicorn logger
    # works with uvicorn==0.25.0
    uvicorn_loggers_names = list(
        filter(lambda x: x.startswith("uvicorn"), logging.root.manager.loggerDict)
    )
    sqlalchemy_loggers_names = list(
        filter(lambda x: x.startswith("sqlalchemy"), logging.root.manager.loggerDict)
    )
    loggers_names = loggers_names or [
        *uvicorn_loggers_names,
        *sqlalchemy_loggers_names,
    ]

    for _logger in get_loggers_by_names(loggers_names):
        _logger.handlers = []

    overwrite_loggers_names = overwrite_loggers_names or [
        "uvicorn",
        # "uvicorn.error",
        "uvicorn.access",
        "sqlalchemy",
    ]
    for _logger in get_loggers_by_names(overwrite_loggers_names):
        _logger.handlers = [InterceptHandler()]

    # set logs output, level and format
    _loguru_logger.configure(
        handlers=[{"sink": sys.stdout, "level": logging.DEBUG, "format": format_record}]
    )


def init_loguru_logger(
    app: FastAPI,
    loggers_names: Optional[list[str]] = None,
    overwrite_loggers_names: Optional[list[str]] = None,
) -> None:
    logging.getLogger("passlib").setLevel(logging.ERROR)
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    Logger().logger = _loguru_logger
    app.add_event_handler(
        "startup",
        lambda: replace_logging_to_loguru(
            loggers_names=loggers_names, overwrite_loggers_names=overwrite_loggers_names
        ),
    )
