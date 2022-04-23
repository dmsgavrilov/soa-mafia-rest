import logging

from app.db.database import SessionLocal
from db.init_db import create_first_user

logger = logging.getLogger(__name__)


def init():
    db = SessionLocal()
    create_first_user(db)


def main() -> None:
    print("Creating initial data")
    init()
    print("Initial data created")


if __name__ == "__main__":
    main()
