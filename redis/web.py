# encoding: utf-8

import time
import json

class Inventory(object):
    def get(self, pk):
        return 'row'


def check_token(conn, token):
    return conn.hget('login:', token)


def update_token(conn, token, user, item=None):
    timestamp = int(time.time())
    conn.hset('login:', token, user)
    conn.zadd('recent:', timestamp, token)
    if item:
        conn.zadd('viewed:' + token, timestamp, item)
        conn.zremrangebyrank('viewed:' + token, 0, -26)
        # with most-viewed item having the lowest score
        conn.zincrby('viewed:', item, -1)

def rescale_viewed(conn):
    while not QUIT:
        # remove any item not in the top 20,000 viewed items.
        conn.zremrangebyrank('viewed:', 20000, -1)
        # rescale all counts to be 1/2 what they were before
        conn.zinterstore('viewed:', {'viewed': .5})
        time.sleep(300)


QUIT = False
LIMIT = 10000000

def clean_sessions(conn):
    while not QUIT:
        size = conn.zcard('recent:')
        if size <= LIMIT:
            time.sleep(1)
            continue
        end_index = min(size - LIMIT, 100)
        tokens = conn.zrange('recent:', 0, end_index - 1)

        session_keys = []
        for t in tokens:
            session_keys.append('viewed:' + t)
            session_keys.append('cart:' + t)

        conn.delete(*session_keys)
        conn.hdel('login:', *tokens)
        conn.zrem('recent:', *tokens)


def add_to_cart(conn, session, item, count):
    if count <= 0:
        conn.hrem('cart:' + session, item)
    else:
        conn.hset('cart:' + session, item, count)

def can_cache(conn, request):
    extract_item_id = lambda r: "id"
    is_dynamic = lambda r: False

    item_id = extract_item_id(request)
    if not item_id or is_dynamic(request):
        return False
    rank = conn.zrank('viewed:', item_id)
    return rank is not None and rank < 10000


def hash_request(request):
    return 'request_' + str(request)


def cache_request(conn, request, callback):
    if not can_cache(conn, request):
        return callback(request)

    page_key = 'cache:' + hash_request(request)
    content = conn.get(page_key)

    if not content:
        content = callback(request)
        conn.setex(page_key, content, 300)

    return content

def schedule_row_cache(conn, row_id, delay):
    conn.zadd('delay:', delay, row_id)
    conn.zadd('schedule:', int(time.time()), row_id)


def cache_rows(conn):
    while not QUIT:
        n = conn.zrange('schedule:', 0, 0, withscores=True)
        now = int(time.time())

        if not n or n[0][1] > now:
            time.sleep(.05)
            continue

        row_id = n[0][0]

        # get the delay before next schedule
        delay = conn.zscore('delay:', row_id)

        # this item should not be cached, remove it from cache
        if delay <= 0:
            conn.zrem('delay:', row_id)
            conn.zrem('schedule:', row_id)
            conn.delete('inv:' + row_id)
            continue

        _cache_row(conn, row_id, delay)

def _cache_row(conn, row_id, delay):
    now = int(time.time())
    row = Inventory.get(row_id)
    conn.zadd('schedule:', now + delay, row_id)
    conn.set('inv:' + row_id, json.dumps(row.to_dict()))
