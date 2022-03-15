from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.core.auth.jwt import auth_jwt
from backend.core.auth.shemas import TokenPair, AccessToken

token_router = APIRouter()


@token_router.post("/token", response_model=TokenPair)
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Generates JWT token pair: access token and refresh token
    """
    user = await auth_jwt.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return auth_jwt.generate_token_pair(user)


@token_router.post("/token/refresh", response_model=AccessToken)
async def generate_new_access_token(token: str):
    """
    Uses refresh token to generate new access token
    """
    access_token = auth_jwt.create_access_token_from_refresh_token(refresh_token=token)
    return AccessToken(access_token=access_token)
