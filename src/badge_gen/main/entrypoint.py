import logging

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from badge_gen.handlers import leetcode_router
from badge_gen.main.config import Config, load_config
from badge_gen.main.di.providers import CacheProvider, HTTPProvider, TemplateProvider


def create_app() -> FastAPI:
    logging.basicConfig(level=logging.DEBUG)

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


app = create_app()
