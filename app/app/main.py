import logging

from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware

import uvicorn

from app.api import api_router
from app.config import settings


uvicorn_logger = logging.getLogger("uvicorn")
logger.handlers = uvicorn_logger.handlers
logger.setLevel(logging.DEBUG)

app = FastAPI(
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    title=settings.APP_TITLE
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(f"{settings.API_V1_PREFIX}/for_download", StaticFiles(directory="for_download"), name="for_download")

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
