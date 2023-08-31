import json
import os
import random
import string

import redis


def random_string(x: int = 10):
    return "".join(random.choices(string.hexdigits, k=x))


redis_instance = redis.StrictRedis(host=os.getenv('REDIS_HOST'),
                                   port=os.getenv('REDIS_PORT'), db=0)


def manage_items_to_redis_save(*args):
    key = 'articles'
    value = args[0]
    value_str = json.dumps(value)
    redis_instance.set(key, value_str)
    return {
        'msg': f"{key} successfully set to {value}"
    }
