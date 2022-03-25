from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel

from backend.core.app.models import User, Project, TeamMember, Task

User_Pydantic = pydantic_model_creator(User, name="User", exclude=("team_member",))


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


Project_Pydantic = pydantic_model_creator(Project, name="Project", exclude=("team_members__assigned_to",))


class ProjectCreate(PydanticModel):
    name: str = Field(...)
    description: Optional[str]

    class Config:
        title = "ProjectCreate"


TeamMember_Pydantic = pydantic_model_creator(TeamMember, name="TeamMember", exclude=("project", "assigned_to"))


class TeamMemberCreate(PydanticModel):
    user_id: int = Field(...)
    role: Optional[str]

    class Config:
        title = "TeamMemberCreate"


class TeamMemberUpdate(PydanticModel):
    role: str

    class Config:
        title = "TeamMemberUpdate"


class ColumnCreate(PydanticModel):
    title: str = Field(...)

    class Config:
        title = "ColumnCreate"


Task_Pydantic = pydantic_model_creator(Task, name="Task", exclude=("column", "column_id", "assignee__project"))


class TaskCreate(PydanticModel):
    title: str = Field(...)
    description: Optional[str]

    class Config:
        title = "TaskCreate"


class TaskUpdate(TaskCreate):
    title: Optional[str]
    column_id: int = Field(...)

    class Config:
        title = "TaskUpdate"


class TaskAssign(PydanticModel):
    assignee_id: int = Field(...)

    class Config:
        title = "TaskAssign"
