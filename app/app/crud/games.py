from app.crud.base import CRUDBase
from app.models import Game
from app.schemas.games import CreateGame, UpdateGame


class CRUDGame(CRUDBase[Game, CreateGame, UpdateGame]):
    pass


game = CRUDGame(Game)
