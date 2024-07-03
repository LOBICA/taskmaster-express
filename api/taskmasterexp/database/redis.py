import redis.asyncio as redis

from taskmasterexp.settings import REDIS_URL


async def get_redis():
    client = redis.from_url(REDIS_URL)
    async with client as conn:
        await conn.ping()
        yield client
    await client.aclose()
