from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config import get_settings

engine = create_async_engine(f"{get_settings().postgres.uri}")
