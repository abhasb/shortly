from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError

from app.core.constants import CACHE_TTL
from app.core.db import AsyncSessionLocal
from app.core.providers import get_id_provider
from app.core.redis import redis_client
from app.core.services import ShortenerService
from app.core.utils import is_url
from app.models.url import Url
from app.schemas.main import URLShortnerRequest, URLShortnerResponse

router = APIRouter()


def get_shortener_service():
    return ShortenerService(get_id_provider())


@router.post(
    "/short", 
    response_model=URLShortnerResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Create a short URL"
)
async def create_short_url(
    request: URLShortnerRequest,
    service: ShortenerService = Depends(get_shortener_service)
):
    if not is_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid URL provided")

    short_code = await service.generate_code()

    async with AsyncSessionLocal() as db:
        try:
            url_obj = Url(original_url=request.url, short_code=short_code, expiration_time=request.expiration_time)
            db.add(url_obj)
            await db.commit()
            await db.refresh(url_obj)
            await redis_client.setex(short_code, CACHE_TTL, request.url)
            return url_obj
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Short code already exists")
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{short_code}", 
    status_code=status.HTTP_302_FOUND, 
    summary="Redirect to original URL"
)
async def redirect_to_url(short_code: str):
    cached_url = await redis_client.get(short_code)
    if cached_url:
        return RedirectResponse(url=str(cached_url), status_code=status.HTTP_302_FOUND)

    async with AsyncSessionLocal() as db:
        url_obj = await db.get(Url, short_code)
        if not url_obj:
            raise HTTPException(status_code=404, detail="Short URL not found")
        original_url = str(url_obj.original_url)
        await redis_client.setex(short_code, CACHE_TTL, original_url)
        return RedirectResponse(url=original_url, status_code=status.HTTP_302_FOUND)
