from fastapi import Depends

from backend.config import settings
from backend.core.app.models import User
from backend.core.auth.jwt import auth_jwt


async def current_user(token: str = Depends(settings.oauth2_scheme)) -> User:
    token_data = auth_jwt.decode_token(token)
    user = await User.get(id=token_data.get("id"))
    return user
