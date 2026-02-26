from app.core.providers import IDProvider
from app.core.utils import encode_base62


class ShortenerService:
    """
    Pure logic layer: Converts a unique ID into a base62 string.
    """
    def __init__(self, id_provider: IDProvider):
        self.id_provider = id_provider

    def generate_code(self) -> str:
        unique_id = self.id_provider.get_next_id()
        return encode_base62(unique_id)