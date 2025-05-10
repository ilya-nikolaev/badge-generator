import json
import logging

import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)

_GQL_URL = "https://leetcode.com/graphql"
_GQL_QUERY = """
query getUserStats($username: String!) {
    matchedUser(username: $username) {
        username
        submitStats: submitStatsGlobal {
            acSubmissionNum {
                difficulty
                count
            }
        }
    }
}"""


class ProblemStats(BaseModel):
    easy: int
    medium: int
    hard: int


class LeetCodeProfile(BaseModel):
    username: str
    solved: ProblemStats


async def get_profile(
    client: httpx.AsyncClient,
    username: str,
) -> LeetCodeProfile:
    response = await client.post(
        _GQL_URL,
        json={"query": _GQL_QUERY, "variables": {"username": username}},
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()
    logger.debug("Got response: %s", json.dumps(data))

    user_data = data["data"]["matchedUser"]
    submissions = user_data["submitStats"]["acSubmissionNum"]
    stats = {s["difficulty"]: s["count"] for s in submissions}

    return LeetCodeProfile(
        username=user_data["username"],
        solved=ProblemStats(
            easy=stats.get("Easy", 0),
            medium=stats.get("Medium", 0),
            hard=stats.get("Hard", 0),
        ),
    )
