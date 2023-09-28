import json
import os
import secrets
import string

import redis
import requests
from requests import ConnectTimeout

from project.celery import app


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
        return json.loads(str(retrieved_data_string))


@app.task
def news_api():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "ru",
        "apiKey": os.getenv("NEWS_API_KEY"),
    }
    articles = CacheRedis().manage_items_to_redis_get("articles")
    if articles:
        return articles
    try:
        response = requests.get(url, params=params, timeout=(1.5, 2))
        data = response.json()
        CacheRedis().manage_items_to_redis_save(key="articles", data=data)
        return data
    except ConnectTimeout:
        return {
            "message": "Request has timed out",
        }
