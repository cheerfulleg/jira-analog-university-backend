from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from starlette.responses import HTMLResponse
from tortoise.contrib.fastapi import register_tortoise

from backend.config import settings
from backend.config.settings import templates
from backend.config.tortoise_conf import TORTOISE_ORM
from backend.core.urls import register_views

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Renders default page
    """
    return templates.TemplateResponse("index.html", {"request": request})


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    modules={"models": settings.MODELS_LIST},
    generate_schemas=True,
    add_exception_handlers=True,
)

register_views(app)
add_pagination(app)
