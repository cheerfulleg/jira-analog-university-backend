from pydantic import EmailStr, Field, BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel

from backend.core.app.models import User

User_Pydantic = pydantic_model_creator(User, name="User")


class BaseUser(PydanticModel):
    email: EmailStr = Field(..., description="unique user email")
    first_name: str = Field(...)
    last_name: str = Field(...)


class UserCreate_Pydantic(BaseUser):
    """
    User creation schema
    """

    password: str = Field(...)

    class Config:
        title = "UserCreate"


class ResetPassword(BaseModel):
    password: str
