import json
import os
import secrets
import string

import redis
import requests
from requests import ConnectTimeout

from project.celery import app


def random_string(quantity: int = 10):
    return "".join(secrets.choice(string.hexdigits) for _ in range(quantity))


def random_username(quantity: int = 10):
    return "".join(secrets.choice(string.ascii_letters) for _ in range(quantity))


class Redis:
    def __init__(self):
        self.redis_instance = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            db=0,
        )

    def manage_items_to_redis_save(self, key, data=None):
        value = json.dumps(data)
        self.redis_instance.set(key, value, ex=60 * 10)
        return {"msg": f"{key} successfully set to {value}"}

    def manage_items_to_redis_get(self, key):
        retrieved_data_string = self.redis_instance.get(key)
        if not retrieved_data_string:
            return None
        return json.loads(retrieved_data_string)


@app.task
def news_api():
    key = "articles"
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "ru",
        "apiKey": os.getenv("NEWS_API_KEY"),
    }
    articles = redis_client.manage_items_to_redis_get(key=key)
    if articles:
        return articles
    try:
        response = requests.get(url, params=params, timeout=(1.5, 2))
        data = response.json()
        redis_client.manage_items_to_redis_save(key=key, data=data)
        return data
    except ConnectTimeout:
        return {
            "message": "Request has timed out",
        }


redis_client = Redis()
