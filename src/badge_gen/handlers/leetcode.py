import logging
from typing import Annotated

import httpx
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, Path, Response, status
from jinja2 import Environment

from badge_gen.fetchers.leetcode import get_profile
from badge_gen.main.config import Config

logger = logging.getLogger(__name__)

leetcode_router = APIRouter(prefix="/leetcode", route_class=DishkaRoute)


@leetcode_router.get(
    "/40/{username}",
    responses={
        status.HTTP_200_OK: {
            "content": {"image/svg+xml": {}},
            "description": "Successfully generated badge in SVG format",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Access denied, username is not in white list",
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
