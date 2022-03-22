from fastapi import Depends, HTTPException
from starlette import status

from backend.config import settings
from backend.core.app.models import User, TeamMember
from backend.core.auth.jwt import auth_jwt


async def current_user(token: str = Depends(settings.oauth2_scheme)) -> User:
    token_data = auth_jwt.decode_token(token)
    user = await User.get(id=token_data.get("id"))
    return user


async def is_team_member(project_id: int, user: User = Depends(current_user)) -> TeamMember:
    if team_member := await TeamMember.filter(project_id=project_id, user_id=user.id).first():
        return team_member
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not found",
    )
