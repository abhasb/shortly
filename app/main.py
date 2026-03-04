from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import api_router
from app.core.db import engine, Base
import app.models.url


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


class ShortlyApp(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(
            title="Shortly API",
            description="Shortly URL Shortener Application API",
            version="0.1.0",
            lifespan=lifespan,
            *args,
            **kwargs,
        )

        self.__setup_routes()

    def __setup_routes(self):
        self.include_router(api_router)


app = ShortlyApp()