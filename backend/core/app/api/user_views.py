from backend.core.auth.permissions import current_user
from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi_mail import MessageSchema
from starlette.responses import JSONResponse

from backend.config.settings import fm
from backend.core.auth.jwt import auth_jwt
from backend.core.app.models import User
from backend.core.app.schemas import User_Pydantic, UserCreate_Pydantic, ResetPassword

user_router = APIRouter()


@user_router.post("", response_model=User_Pydantic, status_code=201)
async def create_user(new_user: UserCreate_Pydantic):
    """
    Register new user
    - **email**: string 120 characters (validating)
    - **password_hash**: any password that will be hashed
    """
    password_hash = User.create_password_hash(new_user.password)
    user_obj = await User.create(
        email=new_user.email, password=password_hash, first_name=new_user.first_name, last_name=new_user.last_name
    )
    return await User_Pydantic.from_tortoise_orm(user_obj)


@user_router.post("/reset-password")
async def request_reset_password(email: str, background_tasks: BackgroundTasks):
    user = await User.get(email=email)

    payload = {"id": user.id}
    reset_token = auth_jwt.create_access_token(payload)
    html = (
        "\nHi, you requested to reset your account password\n"
        "Please, click the link to change your password\n"
        "http://127.0.0.1:8000/users/reset-password/{} \n"
    ).format(reset_token)

    message = MessageSchema(subject="Reset your password", recipients=[email], body=html, subtype="html")

    background_tasks.add_task(fm.send_message, message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


@user_router.post("/reset-password/{token}")
async def reset_password(token: str, data: ResetPassword):
    payload = auth_jwt.decode_token(token)
    password_hash = User.create_password_hash(data.password)
    await User.filter(id=payload.get("id")).update(password=password_hash)
    return JSONResponse(status_code=200, content={"detail": "password was changed"})


@user_router.get("", response_model=User_Pydantic)
async def get_user_profile(user: User = Depends(current_user)):
    """
    Get current user details
    """
    return await User_Pydantic.from_tortoise_orm(user)
