# encoding: utf-8

import bisect
import time
import uuid
import contextlib
from datetime import datetime

import redis

PRECISIONS = [1, 5, 60, 300, 3600, 18000, 86400]
SAMPLE_COUNT = 10

@contextlib.contextmanager
def access_time(conn, context):
    start = time.time()
    yield
    delta = time.time() - start
    stats = update_stats(conn, context, 'AccessTime', delta)
    average = stats[1] / stats[0]

    pipe = conn.pipeline(True)
    pipe.zadd('slowest:AccessTime', context, average)
    pipe.zremrangebyrank('slowest:AccessTime', 0, -101)
    pipe.execute()


def update_counter(conn, name, count=1, now=None):
    now = now or time.time()
    pipe = conn.pipeline()
    for prec in PRECISIONS:
        pnow = int(now / prec) * prec
        print(pnow, now, prec)
        k = "%s:%s" % (prec, name)
        pipe.zadd("known:", k, 0)
        pipe.hincrby("count:" + k, pnow, count)
    pipe.execute()


def get_counter(conn, name, precision):
    k = '%s:%s' % (precision, name)
    data = conn.hgetall('count:' + k)
    to_return = []
    for key, value in data.iteritems():
        to_return.append((int(key), int(value)))
    to_return.sort()
    return to_return

conn = redis.Redis()
# update_counter(conn, "test")
print(get_counter(conn, 'test', 5))

# cleaning out old counters

def clean_counters(conn):
    pipe = conn.pipeline(True)
    start = time.time()
    index = 0
    while index < conn.zcard("known:"):
        hsh = conn.zrange("known:", index, index)
        index += 1
        if not hsh:
            break
        hsh = hsh[0]
        prec = int(hsh.partition(":")[0])
        bprec = int(prec // 60) or 1

        # if passes % bprec:
        #     continue

        hkey = "count:" + hsh
        cutoff = time.time() - SAMPLE_COUNT * prec
        samples = map(int, conn.hkeys(hkey))
        samples.sort()
        remove = bisect.bisect_right(samples, cutoff)

        if remove:
            conn.hdel(hkey, *samples[:remove])
            if remove == len(samples):
                try:
                    pipe.watch(hkey)
                    if not pipe.hlen(hkey):
                        pipe.multi()
                        pipe.zrem("known:", hsh)
                        pipe.execute()
                        index -= 1
                    else:
                        pipe.unwatch()
                except redis.exceptions.WatchError:
                    pass
    # passes += 1
    # duration = min(int(time.time() - start) + 1, 60)

def update_stats(conn, context, type, value, timeout=5):
    destination = "stats:%s:%s" % (context, type)
    pipe = conn.pipeline(True)
    now = datetime.utcnow().timetuple()
    now = datetime(*now[:4]).isoformat()
    tkey1 = str(uuid.uuid4())
    tkey2 = str(uuid.uuid4())

    # 这里使用并集取得来做 aggregate 操作, 然后再做删除
    # 好处是利用了 zunionstore 的特性， 操作全在 redis 里， 保证了事务
    # 坏处是额外创建二个临时的key用做存储
    pipe.zadd(tkey1, 'min', value)
    pipe.zadd(tkey2, 'max', value)

    pipe.zunionstore(destination, [destination, tkey1], aggregate='min')
    pipe.zunionstore(destination, [destination, tkey2], aggregate='max')
    pipe.delete(tkey1, tkey2)
    pipe.zincrby(destination, 'count')
    pipe.zincrby(destination, 'sum', value)
    pipe.zincrby(destination, 'sumsq', value*value)
    return pipe.execute()[-3:]

with access_time(conn, 'clean') as _:
    clean_counters(conn)


def process_view(conn, request, callback):
    with access_time(conn, request.path):
        return callback(request)

