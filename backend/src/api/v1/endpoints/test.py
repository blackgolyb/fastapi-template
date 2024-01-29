from fastapi import APIRouter, Request

from src.api.dependencies import SessionDep, SettingsDep
from src.crud.user import UserCRUD
from src.models.user import User, UserCreate, UserUpdate
from src.utils.logger import logger

router = APIRouter()


@router.get("/")
async def index(
    request: Request,
    settings: SettingsDep,
) -> dict[str, str]:
    logger.info(settings.core.secret_key)
    logger.info(settings.core.debug)
    logger.info(settings.postgres.user)
    logger.info(settings.postgres.uri)
    logger.info("PONG")
    logger.info(type(logger.logger))
    logger.info(logger.logger)
    logger.info(id(logger.logger))
    logger.info(id(logger))
    return {"ping": "pong!"}


@router.post("/create_user")
async def test_user_create(user_creation_data: UserCreate, session: SessionDep) -> User:
    logger.debug(user_creation_data.model_dump)

    crud = UserCRUD(session)

    user = await crud.create(user_creation_data)
    logger.debug(f"last user id: {user.id}")

    await crud.delete(user.id)

    user = await crud.create(user_creation_data)
    logger.debug(f"new user id: {user.id}")

    changed_data = UserUpdate(username=user.username + "_update")
    user = await crud.update(user, changed_data)

    find_user = await crud.find(user.id)
    logger.debug(f"{find_user = }")

    return user
