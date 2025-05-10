import logging

import httpx
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, Response
from jinja2 import Environment

from badge_gen.fetchers.leetcode import get_profile
from badge_gen.main.config import Config

logger = logging.getLogger(__name__)

leetcode_router = APIRouter(prefix="/leetcode", route_class=DishkaRoute)


@leetcode_router.get("/40/{username}")
async def get_40(
    username: str,
    *,
    config: FromDishka[Config],
    env: FromDishka[Environment],
    client: FromDishka[httpx.AsyncClient],
) -> Response:
    if username not in config.access.white_list["leetcode"]:
        raise HTTPException(403, "Username is not in white list")

    profile = await get_profile(client, username)
    content = env.get_template("leetcode-40.svg").render(
        username=profile.username,
        easy=profile.solved.easy,
        medium=profile.solved.medium,
        hard=profile.solved.hard,
    )

    return Response(content, status_code=200, media_type="image/svg+xml")
