import time

from fastapi import APIRouter

from fastapi_cache.decorator import cache

import redis


redis = redis.Redis(host='localhost', port=6379, decode_responses=True)

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.get("/long_operation")
@cache(expire=30)
async def get_long_op():
    time.sleep(2)
    await redis.set("key", "value")
    value = await redis.get("key")
    return {"message": value}



