from typing import AsyncGenerator

from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db import engine

# expire_on_commit=False will prevent attributes from being expired after commit.
AsyncSessionFactory = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Dependency
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        # logger.debug(f"ASYNC Pool: {engine.pool.status()}")
        yield session
