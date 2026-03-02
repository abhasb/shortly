from abc import ABC, abstractmethod
from collections import deque
from functools import lru_cache
from typing import cast

import redis as redis_module

from app.core.config import settings


class IDProvider(ABC):
    @abstractmethod
    def get_next_id(self) -> int:
        pass


class RedisIDProvider(IDProvider):

    def __init__(self, redis_client: redis_module.Redis, key: str = "shortly:id_counter"):
        self._client = redis_client
        self._key = key

    def get_next_id(self) -> int:
        return cast(int, self._client.incr(self._key))


class BatchedRedisIDProvider(IDProvider):
    """
    ID provider that reserves IDs from Redis in batches.

    On each get_next_id() call it pops from an in-memory deque.
    When the deque is empty it calls INCRBY once to claim the next
    batch_size IDs atomically, then refills the deque.
    """

    def __init__(self, redis_client: redis_module.Redis, key: str = "shortly:id_counter", batch_size: int = 100):
        self._client = redis_client
        self._key = key
        self._batch_size = batch_size
        self._ids: deque[int] = deque()

    def get_next_id(self) -> int:
        if not self._ids:
            self._refill()
        return self._ids.popleft()

    def _refill(self) -> None:
        # INCRBY returns the counter value after adding batch_size,
        # so we own the range [end - batch_size + 1, end] exclusively.
        end = cast(int, self._client.incrby(self._key, self._batch_size))
        start = end - self._batch_size + 1
        self._ids.extend(range(start, end + 1))


@lru_cache(maxsize=1)
def get_id_provider() -> IDProvider:
    print(settings.ID_PROVIDER_TYPE)
    if settings.ID_PROVIDER_TYPE == "redis":
        from app.core.redis import redis_client
        return RedisIDProvider(redis_client)
    if settings.ID_PROVIDER_TYPE == "redis_batched":
        from app.core.redis import redis_client
        return BatchedRedisIDProvider(redis_client)

    raise ValueError(f"Unsupported provider: {settings.ID_PROVIDER_TYPE}")
