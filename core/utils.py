import json
import os
import secrets
import string

import redis


def random_string(x: int = 10):
    return "".join(secrets.choice(string.hexdigits) for _ in range(x))


redis_instance = redis.StrictRedis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    db=0,
)


def manage_items_to_redis_save(key, data):
    value = data.get(key)
    value_str = json.dumps(value)
    redis_instance.set(key, value_str, ex=60)
    return {"msg": f"{key} successfully set to {value}"}
