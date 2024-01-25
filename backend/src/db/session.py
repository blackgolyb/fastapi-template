from asyncio import current_task
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.config import get_settings


class MultitonIfRequiredMeta(type):
    """Metaclass that provides Multiton pattern
    if instance_name_ passed with object creation.
    Else object will be created normal.
    """

    _instances: dict[Any, dict[str, Any]] = {}

    def __call__(
        cls, *args: Any, instance_name_: str | None = None, **kwargs: Any
    ) -> Any:
        if instance_name_ is None:
            return super().__call__(*args, **kwargs)

        cls_dict = cls._instances.get(cls, {})
        if instance_name_ not in cls_dict:
            if cls not in cls._instances:
                cls._instances[cls] = {}

            instance = super().__call__(*args, **kwargs)
            cls_dict[instance_name_] = instance
            cls._instances[cls] = cls_dict

        return cls._instances[cls][instance_name_]


class DatabaseHP(metaclass=MultitonIfRequiredMeta):
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )

        # expire_on_commit=False will prevent attributes from being expired after commit.
        self.get_session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    def get_scoped_session(self) -> async_scoped_session[AsyncSession]:
        session = async_scoped_session(
            session_factory=self.get_session,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.get_session() as session:
            yield session

    async def scoped_session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.get_scoped_session()
        yield session  # type: ignore
        await session.close()


# Dependency
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    settings = get_settings()
    db = DatabaseHP(
        url=f"{settings.postgres.uri}",
        echo=settings.core.debug,
        instance_name_=settings.core.project_name,
    )  # type: ignore
    session = db.get_scoped_session()
    yield session  # type: ignore
    await session.close()
