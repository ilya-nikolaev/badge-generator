import logging

import uvicorn.logging
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from badge_gen.handlers import leetcode_router
from badge_gen.main.config import Config, load_config
from badge_gen.main.di.providers import (
    CacheProvider,
    HTTPProvider,
    TemplateProvider,
)


def create_app() -> FastAPI:
    formatter = uvicorn.logging.DefaultFormatter(
        fmt="%(levelprefix)s %(asctime)s %(module)s %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    logger.addHandler(handler)

    config = load_config()

    container = make_async_container(
        HTTPProvider(),
        TemplateProvider(),
        CacheProvider(),
        context={
            Config: config,
        },
    )

    app = FastAPI()
    setup_dishka(container, app)

    app.include_router(leetcode_router)

    return app
