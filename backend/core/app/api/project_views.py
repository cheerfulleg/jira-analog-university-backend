from fastapi import APIRouter, Depends

from backend.core.app.models import Project, User, TeamMember, Column
from backend.core.app.schemas import Project_Pydantic, ProjectCreate, TeamMemberCreate, ColumnCreate
from backend.core.auth.permissions import current_user, is_team_member

project_router = APIRouter()


@project_router.get("", response_model=list[Project_Pydantic])
async def get_all_projects_list(user: User = Depends(current_user)):
    return await Project_Pydantic.from_queryset(Project.all())


@project_router.get("/my", response_model=list[Project_Pydantic])
async def get_my_projects_list(user: User = Depends(current_user)):
    return await Project_Pydantic.from_queryset(Project.filter(team_members__user_id__in=[user.id]))


@project_router.post("", response_model=Project_Pydantic)
async def create_project(project: ProjectCreate, user: User = Depends(current_user)):
    project_obj = await Project.create(**project.dict())
    await TeamMember.create(user_id=user.id, project_id=project_obj.id)
    return await Project_Pydantic.from_tortoise_orm(project_obj)


@project_router.get("/{project_id}", response_model=Project_Pydantic)
async def get_project_detail(project_id: int, user: User = Depends(current_user)):
    return await Project_Pydantic.from_tortoise_orm(Project.get(id=project_id))


@project_router.post("/{project_id}/add-member", response_model=Project_Pydantic)
async def add_team_member(
    project_id: int, new_team_member: TeamMemberCreate, team_member: TeamMember = Depends(is_team_member)
):
    await TeamMember.create(**new_team_member.dict(), project_id=project_id)
    return await Project_Pydantic.from_queryset_single(Project.get(id=project_id))


@project_router.post("/{project_id}/column", response_model=Project_Pydantic)
async def create_project_column(
    project_id: int, column: ColumnCreate, team_member: TeamMember = Depends(is_team_member)
):
    await Column.create(**column.dict(), project_id=project_id)
    return await Project_Pydantic.from_queryset_single(Project.get(id=project_id))
