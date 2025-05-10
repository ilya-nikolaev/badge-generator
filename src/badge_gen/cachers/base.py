import abc
import logging

from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


class Cacher(abc.ABC):
    @abc.abstractmethod
    async def _save(self, key: str, value: str) -> None: ...

    @abc.abstractmethod
    async def _load(self, key: str) -> str | None: ...

    async def save_model(self, key: str, model: BaseModel) -> None:
        await self._save(key, model.model_dump_json())

    async def load_model[T: BaseModel](
        self,
        key: str,
        model: type[T],
    ) -> T | None:
        if cache := await self._load(key):
            try:
                return model.model_validate_json(cache)
            except ValidationError:
                logger.exception("Cache validation failed")
        return None
