from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID, uuid4

import pydantic
from pydantic import EmailStr, SecretStr, StringConstraints, field_validator
from pydantic_core.core_schema import FieldValidationInfo
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
    hashed_password: Optional[str] = pydantic.Field(None, validate_default=True)

    @field_validator("hashed_password", mode="after")
    @classmethod
    def get_password_hash(cls, v: Optional[str], info: FieldValidationInfo) -> str:
        if v is not None:
            return v

        raw_password: SecretStr = info.data["password"]
        hashed_password = Hasher.get_data_hash(raw_password.get_secret_value())

        return hashed_password


class UserUpdate(SQLModel):
    email: Optional[EmailStr]
    username: Optional[UsernameStr]
    is_admin: Optional[bool]
    is_active: Optional[bool]


class UserDelete(SQLModel):
    id: UUID
