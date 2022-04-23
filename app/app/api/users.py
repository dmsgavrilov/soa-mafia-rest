from fastapi import (
    APIRouter,
    Depends,
    status,
    Response
)

from sqlalchemy.orm import Session

from app.crud import user as user_crud
from app.models import User
from app.schemas.user import CreateUser, GetUser, GetUsers, UpdateUser

router = APIRouter()


@router.post("", response_model=GetUser)
def create_user(
        data: CreateUser, db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_superuser)
):
    return user_crud.create(db, obj_in=data)


@router.get("", response_model=GetUsers)
def get_users(
        db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 10,
        current_user: User = Depends(deps.get_current_superuser)
):
    users, count = user_crud.get_many_users(db, skip=skip, limit=limit)
    return {"data": users, "count": count}


@router.get("/{user_id}", response_model=GetUser)
def get_user(
        user_id: int,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_superuser)
):
    return user_crud.get_by_id(db, user_id)


@router.patch("/{user_id}", response_model=GetUser)
def update_user(
        user_id: int, data: UpdateUser, db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_superuser)
):
    user = user_crud.get_by_id(db, user_id)
    return user_crud.update_user(db=db, user_db=user, data=data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        user_id: int, db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_superuser)
):
    user_crud.delete_user(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
