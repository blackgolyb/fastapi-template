from typing import Generic, Optional, Type, TypeVar
from uuid import UUID

from loguru import logger
from pydantic import BaseModel
from sqlmodel import SQLModel, delete, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import SelectOfScalar

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    session: AsyncSession
    model: Type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def find(self, id: UUID) -> Optional[ModelType]:
        stmt: SelectOfScalar = select(self.model).where(self.model.id == id)
        logger.debug(f"{type(stmt)}  |  {stmt = }")
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def create(self, data: CreateSchemaType) -> ModelType:
        instance = self.model.from_orm(data)

        self.session.add(instance)
        await self.session.commit()

        return instance

    async def update(self, instance: ModelType, data: UpdateSchemaType) -> ModelType:
        data_dict = data.model_dump(exclude_unset=True)
        for key, value in data_dict.items():
            setattr(instance, key, value)

        self.session.add(instance)
        await self.session.commit()

        return instance

    async def delete(self, id: UUID) -> None:
        async with self.session.begin():
            stmt = delete(self.model).where(self.model.id == id)
            await self.session.execute(stmt)
