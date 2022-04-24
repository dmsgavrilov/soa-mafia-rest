import datetime
import json

from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder

from app.models import Game, User, users_games
from app.crud.users import user as user_crud


async def generate_file(db: Session, user_id: int, filepath: str):
    db_user = user_crud.get_by_id(db, user_id)
    user_data = jsonable_encoder(db_user)
    games = db.query(Game).join(users_games, Game.id == users_games.game_id) \
                          .join(User, user_id == users_games.user_id).all()
    user_data["statistics"] = {"victories": 0, "loses": 0, "time_spent (sec)": 0}
    for game in games:
        if game.status == "mafia won":
            user_data["statistics"]["loses"] += 1
        elif game.status == "citizens won":
            user_data["statistics"]["victories"] += 1
        user_data["statistics"]["time_spent (sec)"] += (game.end_date - game.start_date).seconds
    with open(filepath, "w") as f:
        json.dump(user_data, f)
