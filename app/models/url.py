from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.core.db import Base


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class Url(BaseModel):
    __tablename__ = "urls"

    short_code = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    expiration_time = Column(DateTime, nullable=True)