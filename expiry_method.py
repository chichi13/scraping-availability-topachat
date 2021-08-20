import redis
from datetime import datetime


class LocalStorage:
    def __init__(self):
        self.storage = {}

    def __contains__(self, keyName):
        self.updateKeys(keyName)
        return keyName in self.storage

    def getKey(self, keyName):
        self.updateKeys(keyName)
        return self.storage.get(keyName)

    def setKey(self, keyName, date):
        self.storage[keyName] = datetime.now() + date

    def updateKeys(self, keyName):
        if keyName in self.storage and self.storage[keyName] < datetime.now():
            self.storage.pop(keyName, None)


class RedisStorage:
    def __init__(self):
        self.r = redis.Redis()

    def __contains__(self, keyName):
        return self.r.exists(keyName)

    def setKey(self, keyName, time):
        self.r.setex(keyName, time, value="Temps avant expiration")
