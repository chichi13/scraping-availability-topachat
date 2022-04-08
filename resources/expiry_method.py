from datetime import datetime

import redis

from resources.config import settings


class LocalStorage:
    def __init__(self):
        self.storage = {}

    def __contains__(self, key_name):
        self.update_keys(key_name)
        return key_name in self.storage

    def get_key(self, key_name):
        self.update_keys(key_name)
        return self.storage.get(key_name)

    def set_key(self, key_name, date):
        self.storage[key_name] = datetime.now() + date

    def update_keys(self, key_name):
        if key_name in self.storage and self.storage[key_name] < datetime.now():
            self.storage.pop(key_name, None)


class RedisStorage:
    def __init__(self):
        self.r = redis.Redis(
            host=settings.REDIS_URL,
            socket_connect_timeout=settings.REDIS_SOCKET_TIMEOUT,
        )

    def __contains__(self, key_name):
        return self.r.exists(key_name)

    def set_key(self, key_name, time):
        self.r.setex(key_name, time, value="Time before expiration")
