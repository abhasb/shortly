from abc import ABC, abstractmethod
from functools import lru_cache

from app.core.config import settings


class IDProvider(ABC):
    @abstractmethod
    def get_next_id(self) -> int:
        pass

class RedisIDProvider(IDProvider):
    
    def __init__(self, redis_client, key: str = "shortly:id_counter"):
        """
        :param redis_client: The shared Redis client instance.
        :param key: The Redis key that stores our global counter.
        """
        self.client = redis_client
        self.key = key

    def get_next_id(self) -> int:
        return self.client.incr(self.key)

@lru_cache(maxsize=1)
def get_id_provider()-> IDProvider:
    if settings.ID_PROVIDER_TYPE == "redis":
        from app.core.redis import redis_client
        return RedisIDProvider(redis_client)
    
    raise ValueError(f"Unsupported provider: {settings.ID_PROVIDER_TYPE}")