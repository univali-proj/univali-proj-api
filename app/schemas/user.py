from typing import Annotated, Generic, TypeVar

from pydantic import (BaseModel, ConfigDict, EmailStr, Field, SecretStr, StringConstraints, field_validator,)

from app.models.user import UserRole

UserName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
UserPassword = Annotated[SecretStr, Field(min_length=1)]
NameT = TypeVar("NameT", default=UserName)
ActiveT = TypeVar("ActiveT", default=bool)
RoleT = TypeVar("RoleT", default=UserRole)


class UserBase(BaseModel, Generic[NameT, ActiveT, RoleT]):
    """Compartilha campos com tipos específicos para criação, atualização e resposta."""

    model_config = ConfigDict(extra="forbid")

    name: NameT
    active: ActiveT
    role: RoleT


class UserCreate(UserBase[UserName, bool, UserRole]):
    active: bool = True
    role: UserRole = UserRole.USER
    email: EmailStr = Field(max_length=320)
    password: UserPassword


class UserUpdate(UserBase[UserName | None, bool | None, UserRole | None]):
    """Atualização parcial; campos omitidos permanecem inalterados."""

    name: UserName | None = None
    active: bool | None = None
    role: UserRole | None = None
    password: UserPassword | None = None

    @field_validator("name", "active", "role", "password", mode="before")
    @classmethod
    def reject_null(cls, value: object) -> object:
        if value is None:
            raise ValueError("O campo pode ser omitido, mas não pode ser nulo.")
        return value


class UserResponse(UserBase[UserName, bool, UserRole]):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr = Field(max_length=320)
