from src.models.user import User, UserCreate, UserUpdate

from .base import CRUDBase


class UserCRUD(CRUDBase[User, UserCreate, UserUpdate]):
    model = User
