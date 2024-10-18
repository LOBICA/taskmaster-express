import redis.asyncio as redis

from taskmasterexp.settings import REDIS_URL


async def get_redis():
    if "rediss" in REDIS_URL:
        # Configuration for Heroku
        client = redis.from_url(REDIS_URL, ssl_cert_reqs=None)
    else:
        client = redis.from_url(REDIS_URL)
    async with client as conn:
        await conn.ping()
        yield client
    await client.aclose()
