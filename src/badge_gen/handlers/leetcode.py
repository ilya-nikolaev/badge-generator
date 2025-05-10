import logging
from typing import Annotated

import httpx
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, Path, Response, status
from jinja2 import Environment

from badge_gen.cachers.base import Cacher
from badge_gen.fetchers.leetcode import LeetCodeProfile, get_profile
from badge_gen.main.config import Config

logger = logging.getLogger(__name__)

leetcode_router = APIRouter(prefix="/leetcode", route_class=DishkaRoute)


@leetcode_router.get(
    "/40/{username}",
    status_code=200,
    responses={
        status.HTTP_200_OK: {
            "content": {"image/svg+xml": {}},
            "description": "Successfully generated badge in SVG format",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Access denied, username is not in white list",
        },
        status.HTTP_502_BAD_GATEWAY: {
            "description": "Failed to fetch profile from external server",
        },
    },
    summary="Generate statistics badge for leetcode",
    response_description="SVG image 400x40 px",
)
async def get_40(
    username: Annotated[
        str,
        Path(
            pattern=r"^[a-zA-Z0-9_-]+$",
            example="ilya-nikolaev",
            description="Username (alphanumeric with underscores/dashes)",
        ),
    ],
    *,
    config: FromDishka[Config],
    env: FromDishka[Environment],
    client: FromDishka[httpx.AsyncClient],
    cacher: FromDishka[Cacher],
) -> Response:
    if username not in config.access.white_list["leetcode"]:
        raise HTTPException(403, "Username is not in white list")

    key = f"leetcode:profile:{username}"
    if (profile := await cacher.load_model(key, LeetCodeProfile)) is None:
        try:
            profile = await get_profile(client, username)
            await cacher.save(key, profile.model_dump_json())
        except Exception as e:
            raise HTTPException(502, "Failed to fetch profile") from e

    content = env.get_template("leetcode-40.svg").render(
        username=profile.username,
        easy=profile.solved.easy,
        medium=profile.solved.medium,
        hard=profile.solved.hard,
    )

    return Response(content, media_type="image/svg+xml")
