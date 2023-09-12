import json
import os
import secrets
import string

import redis


def random_string(x: int = 10):
    return "".join(secrets.choice(string.hexdigits) for _ in range(x))


class CacheRedis:
    def __init__(self):
        self.redis_instance = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            db=0,
        )

    def manage_items_to_redis_save(self, key, data=None):
        value = json.dumps(data)
        self.redis_instance.set(key, value, ex=60)
        return {"msg": f"{key} successfully set to {value}"}

    def manage_items_to_redis_get(self, key):
        retrieved_data_string = self.redis_instance.get(key)
        if not retrieved_data_string:
            return None
        return json.loads(retrieved_data_string)
