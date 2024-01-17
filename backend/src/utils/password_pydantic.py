from typing import Annotated

from pydantic import SecretStr, StringConstraints
from pydantic.functional_validators import BeforeValidator
from pydantic_core import PydanticCustomError


def validate_password(value: str) -> str:
    if not any(c.isupper() for c in value):
        raise PydanticCustomError(
            "value_error",
            "Password must have at least one uppercase letter",
        )
    if not any(c.islower() for c in value):
        raise PydanticCustomError(
            "value_error",
            "Password must have at least one lowercase letter",
        )
    if not any(c.isdigit() for c in value):
        raise PydanticCustomError(
            "value_error",
            "Password must have at least one digit",
        )

    return value


PasswordValidator = BeforeValidator(validate_password)


def conpass(
    *,
    min_length: int | None = None,
    max_length: int | None = None,
) -> type[SecretStr]:
    return Annotated[
        SecretStr,
        PasswordValidator,
        StringConstraints(
            min_length=min_length,
            max_length=max_length,
        ),
    ]  # type: ignore
