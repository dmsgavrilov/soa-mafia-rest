from sqlalchemy.orm import Session

from app.config import settings
from app.db.database import Base
from app.db.database import engine
from app.models import User


def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)


def drop_db(db: Session) -> None:
    Base.metadata.drop_all(bind=engine)


def create_first_user(db: Session) -> None:
    user = User(
        nickname="admin",
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
        sex="m"
    )
    db.add(user)
    db.commit()
