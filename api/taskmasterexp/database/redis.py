import redis

from taskmasterexp.settings import REDIS_URL


def get_redis():
    return redis.Redis.from_url(REDIS_URL)
