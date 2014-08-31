# encoding: utf-8
from uuid import uuid4

from redis import Redis

redis = Redis()
qkey = 'queue'

from pickle import loads, dumps

class DelayedResult(object):
    def __init__(self, key):
        self.key = key
        self._rv = None

    @property
    def return_value(self):
        if self._rv is None:
            rv = redis.get(self.key)
            if rv is not None:
                self._rv = loads(rv)
        return self._rv


def queuefunc(f):
    def delay(*args, **kwargs):
        key = "%s:result:%s" % (qkey, str(uuid4()))
        s = dumps((f, key, args, kwargs))
        redis.rpush(qkey, s)
        return DelayedResult(key)
    f.delay = delay
    return f


def queue_daemon(rv_ttl=500):
    while 1:
        msg = redis.blpop(qkey) # block pop
        func, key, args, kwargs = loads(msg[1])

        try:
            rv = func(*args, **kwargs)
        except Exception, e:
            rv = e
        if rv is not None:
            redis.set(key, dumps(rv))
            redis.expire(key, rv_ttl)

# queue_daemon()

@queuefunc
def add(a, b):
    return a + b

# j = add.delay(1, 3)

# print(j.return_value)

