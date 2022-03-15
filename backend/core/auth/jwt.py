from datetime import datetime, timedelta
from typing import Union

import jwt
from fastapi import APIRouter, HTTPException

from backend.config import settings
from backend.core.auth.shemas import TokenPair
from backend.core.app.models import User

router = APIRouter()


class AuthJWT:
    secret = settings.JWT_SECRET

    def create_access_token(self, payload) -> str:
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXP_MINUTES),
            "iat": datetime.utcnow(),
            "scope": "access_token",
            "sub": payload,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token) -> str:
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "access_token":
                return payload["sub"]
            raise HTTPException(status_code=401, detail="Scope for the token is invalid")
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail="Token expired") from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token") from e

    def create_refresh_token(self, payload) -> str:
        payload = {
            "exp": datetime.utcnow() + timedelta(hours=settings.REFRESH_TOKEN_EXP_HOURS),
            "iat": datetime.utcnow(),
            "scope": "refresh_token",
            "sub": payload,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def create_access_token_from_refresh_token(self, refresh_token) -> str:
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "refresh_token":
                username = payload["sub"]
                return self.create_access_token(username)
            raise HTTPException(status_code=401, detail="Invalid scope for token")
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail="Refresh token expired") from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid refresh token") from e

    def generate_token_pair(self, user: User) -> TokenPair:
        payload = {"id": user.id}
        access_token = self.create_access_token(payload=payload)
        refresh_token = self.create_refresh_token(payload=payload)
        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    async def authenticate_user(username: str, password: str) -> Union[bool, User]:
        user = await User.get(email=username)
        if not user:
            return False
        if not user.verify_password(password):
            return False
        return user


auth_jwt = AuthJWT()
