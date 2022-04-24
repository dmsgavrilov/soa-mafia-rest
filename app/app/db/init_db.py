from sqlalchemy.orm import Session

from app.config import settings
from app.crud.users import user as user_crud
from app.db.database import Base
from app.db.database import engine
from app.schemas import CreateUser


def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)


def drop_db(db: Session) -> None:
    Base.metadata.drop_all(bind=engine)


def create_first_user(db: Session) -> None:
    user = user_crud.get_by_email(db, email=settings.ADMIN_EMAIL)
    if not user:
        user_in = CreateUser(
            email=settings.ADMIN_EMAIL,
            nickname=settings.ADMIN_NICKNAME,
            img_url=settings.ADMIN_LOGO,
            password=settings.ADMIN_PASSWORD,
            sex=settings.ADMIN_SEX,
            is_superuser=True,
        )
        user_crud.create(db, obj_in=user_in)
