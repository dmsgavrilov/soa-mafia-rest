import logging

from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.openapi.utils import get_openapi
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
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    title=settings.APP_TITLE
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.APP_TITLE,
        version="0.2.0",
        routes=app.routes
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://ont.by/uploads/wysiwyg/images/nBB9QW9uKw5VHVkE.jpg"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

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
