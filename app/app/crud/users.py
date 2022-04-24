from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase, ModelType
from app.models import User, users_games
from app.schemas.users import CreateUser, UpdateUser
from app.utils.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[User, CreateUser, UpdateUser]):

    def get_many_users(self, db: Session, skip: int = 0, limit: int = 10) -> (List[ModelType], int):
        query = db.query(self.model)
        return query.offset(skip).limit(limit).all(), query.count()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: CreateUser) -> User:
        db_obj = User(
            email=obj_in.email,
            img_url=obj_in.img_url,
            nickname=obj_in.nickname,
            sex=obj_in.sex,
            password=get_password_hash(obj_in.password),
            is_superuser=obj_in.is_superuser
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        for game_id in obj_in.games_ids:
            user_game = users_games(user_id=db_obj.id, game_id=game_id)
            db.add(user_game)
        db.commit()
        return db_obj

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def delete_user(self, db: Session, user_id: int):
        db.query(User).filter_by(id=user_id).delete()
        db.commit()
        return

    def update_user(
            self,
            db: Session,
            user_db: User,
            data: UpdateUser
    ) -> User:
        user = jsonable_encoder(user_db)
        update_data = data.dict(exclude_unset=True)
        for field in user:
            if field in update_data:
                if field == "password":
                    setattr(user_db, "password", get_password_hash(update_data[field]))
                else:
                    setattr(user_db, field, update_data[field])
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return user_db


user = CRUDUser(User)
