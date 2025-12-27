import redis

redis_session = None

def init_redis(redis_url):
    global redis_session
    redis_session = redis.from_url(
        redis_url,
        decode_responses=True,
        socket_connect_timeout=1,
        socket_timeout=1)

def get_redis():
    if redis_session is None:
        raise RuntimeError("Redis is not yet initialized. Call init_redis first.")
    return redis_session
