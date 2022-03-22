from fastapi import APIRouter, Depends

from backend.core.app.models import Project, User, TeamMember, Column, Task
from backend.core.app.schemas import (
    Project_Pydantic,
    ProjectCreate,
    TeamMemberCreate,
    ColumnCreate,
    TaskCreate,
    TaskUpdate,
    TaskAssign,
    TeamMember_Pydantic,
    Task_Pydantic,
)
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
    return await Project_Pydantic.from_queryset_single(Project.get(id=project_id))


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


@project_router.post("/{project_id}/column/{column_id}", response_model=Project_Pydantic)
async def create_project_column_task(
    project_id: int, column_id: int, task: TaskCreate, team_member: TeamMember = Depends(is_team_member)
):
    await Task.create(**task.dict(), column_id=column_id)
    return await Project_Pydantic.from_queryset_single(Project.get(id=project_id))


@project_router.patch("/{project_id}/task/{task_id}", response_model=Project_Pydantic)
async def update_project_column_task(
    project_id: int, task_id: int, task: TaskUpdate, team_member: TeamMember = Depends(is_team_member)
):
    await Task.filter(id=task_id).update(**task.dict(exclude_unset=True))
    return await Project_Pydantic.from_queryset_single(Project.get(id=project_id))


@project_router.get("/{project_id}/team-members", response_model=list[TeamMember_Pydantic])
async def get_project_team_members_list(project_id: int, team_member: TeamMember = Depends(is_team_member)):
    return await TeamMember_Pydantic.from_queryset(TeamMember.filter(project_id=project_id))


@project_router.patch("/{project_id}/task/{task_id}/assign", response_model=Project_Pydantic)
async def assign_task_to_member(
    project_id: int, task_id: int, assignee: TaskAssign, team_member: TeamMember = Depends(is_team_member)
):
    await Task.filter(id=task_id).update(**assignee.dict())
    return await Project_Pydantic.from_queryset_single(Project.get(id=project_id))


@project_router.get("/{project_id}/task/{task_id}", response_model=Task_Pydantic)
async def get_task_detail(project_id: int, task_id: int, team_member: TeamMember = Depends(is_team_member)):
    return await Task_Pydantic.from_queryset_single(Task.get(id=task_id))
