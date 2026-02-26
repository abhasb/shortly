from fastapi import FastAPI
from app.api import api_router
from app.core.db import engine, Base
import app.models.url

Base.metadata.create_all(bind=engine)

class ShortlyApp(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(
            title="Shortly API",
            description="Shortly URL Shortener Application API",
            version="0.1.0",
            *args,
            **kwargs,
        )

        self.__setup_routes()

    def __setup_routes(self):
        self.include_router(api_router)
    
        
app = ShortlyApp()