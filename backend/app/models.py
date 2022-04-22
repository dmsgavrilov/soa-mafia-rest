from sqlalchemy import Table

from app.db.database import Base, metadata


class User(Base):
    __table__ = Table("users", metadata, autoload=True)


class Game(Base):
    __table__ = Table("games", metadata, autoload=True)


class Player(Base):
    __table__ = Table("players", metadata, autoload=True)
