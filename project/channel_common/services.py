import redis
from django.conf import settings


class OnlineController:
    class _User:
        def __init__(self, username, key, redis_instance):
            self.key = key
            self.username = username
            self.redis_instance = redis_instance
            self.connect = self._incr
            self.disconnect = lambda: self._rem() if self._decr() < 1 else 1 if username == 'AnonymousUser' else 0

        def __get__(self) -> float:
            return self.redis_instance.zscore(self.key, self.username)

        def _rem(self) -> int:
            return self.redis_instance.zrem(self.key, self.username)

        def _incr(self) -> float:
            return self.redis_instance.zincrby(self.key, +1, self.username)

        def _decr(self) -> float:
            return self.redis_instance.zincrby(self.key, -1, self.username)

    def __init__(self, key, username=False):
        self.key = key
        self.redis_instance = redis.StrictRedis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        self.user = self._User(username, key, self.redis_instance) if username else None

    @property
    def value(self):
        online = self.redis_instance.zcard(self.key)
        if b'AnonymousUser' in self.redis_instance.zrange(self.key, 0, -1):
            online = online - 1 + self.redis_instance.zscore(self.key, 'AnonymousUser')
        return online

