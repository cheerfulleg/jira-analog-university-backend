from fastapi import FastAPI

from backend.core.app.base_router import base_router
from backend.core.auth.routers import token_router


def register_views(app: FastAPI) -> None:
    app.include_router(token_router, tags=["Authentication"])
    app.include_router(base_router, tags=["Base endpoints"])
