# encoding: utf-8

import redis
import time


# r = redis.Redis(port=6383)
#
# # r.delete('k1')
# # r.delete('k2')
# pipeline = r.pipeline()
#
# n = 1
# for i in xrange(n):
#     pipeline.sadd('k1', i)
#     pipeline.sadd('k2', i+n+1)
#
# pipeline.execute()
#
# r = redis.Redis(port=6380)
# start = time.time()
# r.smembers('k1')
# r.smembers('k2')
# # r.sunion('k1', 'k2')
# print('sunionstore cost %s seconds to finished' % (time.time() - start))


def update_token_pipeline(conn, token, user, item=None):
    ts = time.time()
    pipe = conn.pipeline(False) # non transactions
    pipe.hset('login:', token, user)
    pipe.zadd('recent:', token, ts)
    if item:
        pipe.zadd('viewed:' + token, item, ts)
        pipe.zremrangebyrank('viewed:' + token, 0, -26)
        pipe.zincrby('viewed:', item, -1)
    pipe.execute()


def update_token(conn, token, user, item=None):
    ts = time.time()
    pipe = conn
    pipe.hset('login:', token, user)
    pipe.zadd('recent:', token, ts)
    if item:
        pipe.zadd('viewed:' + token, item, ts)
        pipe.zremrangebyrank('viewed:' + token, 0, -26)
        pipe.zincrby('viewed:', item, -1)
    # pipe.execute()


def benchmark(conn, duration):
    for func in (update_token, update_token_pipeline):
        count = 0
        start = time.time()
        end = start + duration
        while time.time() < end:
            count += 1
            func(conn, 'token_a', 'user_a', item='item_a')
        delta = time.time() - start
        print(func.__name__, count, delta, count/delta)

conn = redis.Redis()
benchmark(conn, 10)
