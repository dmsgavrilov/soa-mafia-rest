from typing import Generic, List, Type, TypeVar

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger

from pydantic import BaseModel

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import Base

ModelType = TypeVar("ModelType", bound=Base)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_many(self, db: Session, skip: int = 0, limit: int = 10) -> (List[ModelType], int):
        query = db.query(self.model)
        return query.offset(skip).limit(limit).all(), query.count()

    def get_by_id(self, db: Session, item_id: int) -> ModelType:
        item = db.query(self.model).get(item_id)
        if not item:
            raise HTTPException(status_code=404)
        return item

    def get_by_ids(self, db: Session, ids: List[int]):
        items = db.query(self.model).filter(self.model.id.in_(ids)).all()
        return items

    def remove_by_id(self, db: Session, item_id: int, model: ModelType = None) -> None:
        if model:
            item = db.query(model).get(item_id)
        else:
            item = db.query(self.model).get(item_id)
        if not item:
            raise HTTPException(status_code=404)
        db.delete(item)
        db.commit()
        return

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            logger.error(str(e))
            raise HTTPException(status_code=500, detail=str(e))

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        with_commit: bool = True
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if with_commit:
            try:
                db.add(db_obj)
                db.commit()
                db.refresh(db_obj)
            except IntegrityError as e:
                logger.error(str(e))
                raise HTTPException(status_code=500, detail=str(e))
        return db_obj
