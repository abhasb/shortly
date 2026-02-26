import redis
from app.core.config import settings

redis_client = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=5, # Don't let the app hang if Redis is down
    health_check_interval=30  # Periodically pings Redis to keep connection alive
)
