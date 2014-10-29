# encoding: utf-8

'''
recent: + user

最近联系人
'''

import bisect
import json
import time
import uuid


def add_update_contact(conn, user, contact):
    ac_list = 'recent:' + user
    pipeline = conn.pipeline(True)
    pipeline.lrem(ac_list, contact)
    pipeline.lpush(ac_list, contact)
    pipeline.ltrim(ac_list, 0, 99)
    pipeline.execute()


def remove_contact(conn, user, contact):
    conn.lrem('recent:' + user, 0, -1)


def fetch_autocomplete_list(conn, user, prefix):
    candidates = conn.lrange('recent:' + user, 0, -1)
    matches = []
    for candidate in candidates:
        if candidate.lower().startswith(prefix):
            matches.append(candidate)
    return matches


valid_characters = '`abcdefghijklmnopqrstuvwxyz{'

def find_prefix_range(prefix):
    posn = bisect.bisect_left(valid_characters, prefix[-1:])
    suffix = valid_characters[(posn or 1) - 1]
    return prefix[:-1] + suffix + '{', prefix + '{'


def worker_watch_queue(conn, queue, callbacks):
    packed = conn.blpop([queue], 30)
    if not packed:
        continue
    name, args = json.loads(packed[1])
    if name not in callbacks:
        # log_error("Unknown callback %s" % name)
        continue
    callbacks[name](*args)


def worker_watch_queues(conn, queues, callbacks):
    pass


def execute_later(conn, queue, name, args, delay=0):
    identifier = str(uuid.uuid4())
    item = json.dumps([identifier, queue, name, args])
    if delay > 0:
        conn.zadd('delayed:', time.time() + delay, item)
    else:
        conn.rpush('queue:' + queue, item)
    return identifier


def poll_queue(conn):
    item = conn.zrange('delayed:', 0, 0, withscores=True) # 取最近的一条记录
    if not item or item[0][1] > time.time():
        return
    item = item[0][0]
    identifier, queue, func, args = json.loads(item)
    locked = acquire_lock(conn, identifier)
    if not locked:
        return
    if conn.zrem('delayed:', item):
        conn.rpush('queue:' + queue, item)
    release_lock(conn, identifier, locked)
