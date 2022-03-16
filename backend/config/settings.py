import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi_mail import ConnectionConfig, FastMail
from pydantic import EmailStr

# Base project settings
BASE_DIR = Path(__file__).parent.parent.parent

DOTENV_PATH = ".env"
load_dotenv(dotenv_path=os.path.join(BASE_DIR, DOTENV_PATH))

APP_NAME = "JIRA Analog"
APP_VERSION = "0.0.1beta"

# Database settings
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")
MODELS_LIST = ["backend.core.app.models"]

# Auth settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT settings
JWT_SECRET = os.getenv("JWT_SECRET")
REFRESH_TOKEN_EXP_HOURS = int(os.getenv("REFRESH_TOKEN_EXP_HOURS"))
ACCESS_TOKEN_EXP_MINUTES = int(os.getenv("ACCESS_TOKEN_EXP_MINUTES"))

# Email settings
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL_HOST_USER"),
    MAIL_PASSWORD=os.getenv("EMAIL_HOST_PASSWORD"),
    MAIL_FROM=EmailStr(os.getenv("EMAIL_HOST_USER")),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME=os.getenv("EMAIL_HOST_USER"),
    MAIL_TLS=True,
    MAIL_SSL=False,
)

fm = FastMail(conf)


templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates/"))
