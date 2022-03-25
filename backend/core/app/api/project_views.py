from fastapi import APIRouter, Depends
from fastapi_mail import MessageSchema
from starlette.background import BackgroundTasks

from backend.config.settings import fm
from backend.core.app.models import Project, User, TeamMember, Column, Task
from backend.core.app.schemas import (
    Project_Pydantic,
    ProjectCreate,
    TeamMemberCreate,
    ColumnCreate,
    TaskCreate,
    TaskUpdate,
    TaskAssign,
    Task_Pydantic,
    User_Pydantic,
    TeamMemberUpdate,
    TeamMember_Pydantic,
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
    await Column.create(title="Backlog", project_id=project_obj.id)
    return await Project_Pydantic.from_tortoise_orm(project_obj)


@project_router.get("/{project_id}", response_model=Project_Pydantic)
async def get_project_detail(project_id: int, user: User = Depends(current_user)):
    return await Project_Pydantic.from_queryset_single(Project.get(id=project_id))


@project_router.post("/{project_id}/member", response_model=TeamMember_Pydantic)
async def add_team_member(
    project_id: int, new_team_member: TeamMemberCreate, team_member: TeamMember = Depends(is_team_member)
):
    team_member_obj = await TeamMember.create(**new_team_member.dict(), project_id=project_id)
    return await TeamMember_Pydantic.from_tortoise_orm(team_member_obj)


@project_router.patch("/{project_id}/member/{member_id}", response_model=Project_Pydantic)
async def edit_team_member(
    project_id: int,
    member_id: int,
    team_member_update: TeamMemberUpdate,
    team_member: TeamMember = Depends(is_team_member),
):
    await TeamMember.filter(id=member_id).update(**team_member_update.dict())
    return await Project_Pydantic.from_queryset_single(Project.get(id=project_id))


@project_router.delete("/{project_id}/member/{member_id}", response_model=Project_Pydantic)
async def delete_team_member(project_id: int, member_id: int, team_member: TeamMember = Depends(is_team_member)):
    await TeamMember.filter(id=member_id).delete()
    return await Project_Pydantic.from_queryset_single(Project.get(id=project_id))


@project_router.post("/{project_id}/column", response_model=Project_Pydantic)
async def create_project_column(
    project_id: int, column: ColumnCreate, team_member: TeamMember = Depends(is_team_member)
):
    await Column.create(**column.dict(), project_id=project_id)
    return await Project_Pydantic.from_queryset_single(Project.get(id=project_id))


@project_router.delete("/{project_id}/column/{column_id}", response_model=Project_Pydantic)
async def delete_project_column(project_id: int, column_id: int, team_member: TeamMember = Depends(is_team_member)):
    await Column.filter(id=column_id).delete()
    return await Project_Pydantic.from_queryset_single(Project.get(id=project_id))


@project_router.post("/{project_id}/column/{column_id}/task", response_model=Project_Pydantic)
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


@project_router.delete("/{project_id}/task/{task_id}", response_model=Project_Pydantic)
async def delete_project_column_task(project_id: int, task_id: int, team_member: TeamMember = Depends(is_team_member)):
    await Task.filter(id=task_id).delete()
    return await Project_Pydantic.from_queryset_single(Project.get(id=project_id))


@project_router.get("/{project_id}/team-members", response_model=list[User_Pydantic])
async def get_project_team_members_list(project_id: int, team_member: TeamMember = Depends(is_team_member)):
    return await User_Pydantic.from_queryset(User.filter(team_member__project=project_id))


@project_router.patch("/{project_id}/task/{task_id}/assign", response_model=Task_Pydantic)
async def assign_task_to_member(
    task_id: int,
    assignee: TaskAssign,
    background_tasks: BackgroundTasks,
    team_member: TeamMember = Depends(is_team_member),
):
    await Task.filter(id=task_id).update(**assignee.dict())

    html = "Check out your new Task"
    member = await TeamMember.filter(assigned_to__in=[task_id]).first()
    email = str(await member.user)
    message = MessageSchema(subject="You was assigned to a new Task", recipients=[email], body=html, subtype="html")
    background_tasks.add_task(fm.send_message, message)

    return await Task_Pydantic.from_queryset_single(Task.get(id=task_id))
