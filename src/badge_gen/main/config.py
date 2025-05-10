import logging
import tomllib
from pathlib import Path

from pydantic import BaseModel

logger = logging.getLogger(__name__)

type Username = str


class AccessConfig(BaseModel):
    white_list: dict[str, list[Username]]


class CacheConfig(BaseModel):
    redis_uri: str


class TemplateConfig(BaseModel):
    path: Path


class Config(BaseModel):
    access: AccessConfig
    cache: CacheConfig
    template: TemplateConfig


def load_config() -> Config:
    config_path = Path.cwd() / ".config" / "config.toml"
    logger.debug("Config path: %s", config_path)

    with config_path.open("rb") as file:
        return Config(**tomllib.load(file))
