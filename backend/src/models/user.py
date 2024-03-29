from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID, uuid4

from pydantic import EmailStr, SecretStr, StringConstraints
from sqlmodel import Field, SQLModel

from src.core.security import Hasher
from src.utils.password_pydantic import PasswordValidator


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True)
    username: str = Field(min_length=3, unique=True)
    hashed_password: str
    is_admin: bool = False
    is_active: bool = False
    date_joined: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None


USERNAME_PATTERN = r"^[a-zA-Z_\d]+$"
UsernameStr = Annotated[
    str,
    StringConstraints(min_length=3, pattern=USERNAME_PATTERN),
]
PasswordSecretStr = Annotated[
    SecretStr,
    PasswordValidator,
    StringConstraints(min_length=8, max_length=32),
]


class UserCreate(SQLModel):
    email: EmailStr
    username: UsernameStr
    password: PasswordSecretStr

    @property
    def hashed_password(self) -> str:
        hashed_password = Hasher.get_data_hash(self.password.get_secret_value())

        return hashed_password


class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    username: Optional[UsernameStr] = None
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None


class UserDelete(SQLModel):
    id: UUID
