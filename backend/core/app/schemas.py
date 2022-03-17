from pydantic import BaseModel, EmailStr, Field, ValidationError, validator
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel

from backend.core.app.models import User

User_Pydantic = pydantic_model_creator(User, name="User")


class PasswordMixin(BaseModel):
    password: str = Field(...)

    @validator("password", pre=True)
    def validate_password(cls, value):
        if len(value) <= 8:
            raise ValueError("password must contain at least 8 characters")
        return value


class BaseUser(PydanticModel):
    email: EmailStr = Field(..., description="unique user email")
    first_name: str = Field(...)
    last_name: str = Field(...)


class UserCreate_Pydantic(BaseUser, PasswordMixin):
    """
    User creation schema
    """

    class Config:
        title = "UserCreate"


class ResetPassword(PasswordMixin):
    pass
