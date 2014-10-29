# encoding: utf-8

import time

import contextlib

PRECISION = [1, 5, 60, 300, 3600, 18000, 86400]

def update_counter(conn, name, count=1, now=None):
    now = now or time.time()
    pipe = conn.pipeline()
    for prec in PRECISION:
        pnow = int(now / prec) * prec
        hash_ = '%s:%s' % (prec, name)
        pipe.zadd('known:', hash_, 0)
        pipe.hincrby('count:%s' % hash_, pnow, count)
    pipe.execute()


def get_counter(conn, name, precision, prefix='count'):
    key = '%s:%s' % (precision, name)
    data = conn.hgetall('%s:%s' % (prefix, key))
    to_return = [
        (int(k), int(v)) for k, v in data.iteritems()
    ]
    to_return.sort()
    return to_return


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


def average_counter(conn, name, precision):
    data = get_counter(conn, name, 1)
    tt = {}

    for k, v in data:
        pnow = int(k/precision) * precision
        if pnow not in tt:
            tt[pnow] = []
        tt[pnow].append(v)

    for k, v in tt.items():
        print(k, v, sum(v), len(v))
        tt[k] = sum(v)/len(v)

    key = '%s:%s' % (precision, name)
    conn.hmset('avg:%s' % key, tt)


def get_stats(conn, context, type):
    key = 'stats:%s:%s' % (context, type)
    data = dict(conn.zrange(key, 0, -1, withscores=True))
    data['average'] = data['sum'] / data['count']
    numerator = data['sumsq'] - data['sum'] ** 2 / data['count']
    data['stddev'] = (numerator / (data['count'] - 1 or 1)) ** .5
    return data


def test():
    import redis
    # import random

    conn = redis.Redis()

    average_counter(conn, 'viewed', 60)
    average_counter(conn, 'viewed', 3600)
    average_counter(conn, 'viewed', 10)
    print(get_counter(conn, 'viewed', 60, 'avg'))
    print(get_counter(conn, 'viewed', 3600, 'avg'))
    print(get_counter(conn, 'viewed', 10, 'avg'))

    # while True:
    #     c = random.randint(1, 10)
    #     print(c)
    #     update_counter(conn, 'viewed', count=c)
    #     time.sleep(1)
    get_counter(conn, 'viewed', 1)

test()
