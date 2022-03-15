from fastapi import APIRouter

from backend.core.app.api.user_views import user_router

base_router = APIRouter()

base_router.include_router(user_router, prefix="/user", tags=["User endpoints"])
