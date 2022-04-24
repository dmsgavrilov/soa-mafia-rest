from fastapi import APIRouter

from app.api import auth, users, games

api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(games.router, prefix="/games", tags=["games"])
