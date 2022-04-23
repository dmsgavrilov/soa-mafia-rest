import os
import secrets

from fastapi.templating import Jinja2Templates


class Settings:
    APP_TITLE = "SOA-MAFIA"
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    FIRST_SUPERUSER: str = "test@test.com"
    FIRST_SUPERUSER_PASSWORD: str = "testtest"

    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_MAX_OVERFLOW = 40

    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URI", "postgresql://postgres:123@localhost:5432")

    MAX_IMAGE_SIZE: int = 450  # kb


templates = Jinja2Templates(directory="./app/templates")

settings = Settings()
