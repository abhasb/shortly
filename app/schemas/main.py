from pydantic import BaseModel, computed_field, Field
from datetime import datetime
from typing import Optional

from app.core.config import settings

class URLShortnerRequest(BaseModel):
    url: str
    expiration_time: Optional[int] = None

class URLShortnerResponse(BaseModel):
    original_url: str
    short_code: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def short_url(self) -> str: 
        return f"{settings.BASE_URL}/{self.short_code}"

    class Config:
        from_attributes = True