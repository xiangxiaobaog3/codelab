# encoding: utf-8

import time

def create_user(conn, login, name):
    llogin = login.lower()
    lock = acquire_lock_with_timeout(conn, 'user:' + llogin)
    if not lock:
        return None

    # 避免登陆重复登陆
    if conn.hget('users:', llogin):
        return None

    id = conn.incr('user:id:')
    pipeline = conn.pipeline(True)
    pipeline.hset('users:', llogin, id)
    pipeline.hmset('user:%s' % id, {
        'login': login,
        'id': id,
        'name': name,
        'followers': 0,
        'following': 0,
        'posts': 0,
        'signup': time.time(),
    })
    pipeline.execute()
    release_lock(conn, 'user:' + llogin, lock)
    return id

def create_status(conn, uid, message, **data):
    pipeline = conn.pipeline(True)
    pipeline.hget('user:%s' % uid, 'login')
    pipeline.incr('status:id:')
    login, id = pipeline.execute()
    if not login:
        return None
    data.update({
        'message': message,
        'posted': time.time(),
        'id': id,
        'uid': uid,
        'login': login,
    })

    pipeline.hmset('status:%s' % id, data)
    pipeline.hincrby('user:%s' % uid, 'posts')
    pipeline.execute()
    return id


def get_status_messages(conn, uid, timeline='home:', page=1, count=30):
    statuses = conn.zrevrange(
        "%s%s" % (timeline, uid), (page-1) * count, page * count-1)

    pipeline = conn.pipeline(True)
    for id in statuses:
        pipeline.hgetall('status:%s' % id)

    return filter(None, pipeline.execute())


HOME_TIMELINE_SIZE = 1000

def follow_user(conn, uid, other_uid):
    fkey1 = 'following:%s' % uid
    fkey2 = 'followers:%s' % other_uid

    if conn.zscore(fkey1, other_uid):
        return None

    now = time.time()
    pipeline = conn.pipeline(True)
    pipeline.zadd(fkey1, now, other_uid)
    pipeline.zadd(fkey2, now, uid)

    pipeline.zrevrange('profile:%s' % other_uid,
                      0, HOME_TIMELINE_SIZE-1, withscores=True)
    following, followers, status_and_score = pipeline.execute()[-3:]
    pipeline.hset('user:%s' % uid, 'following', following)
    pipeline.hset('user:%s' % other_uid, 'followers', followers)
    if status_and_score:
        pipeline.zadd('home:%s' % uid, **dict(status_and_score))
    pipeline.zremrangebyrank('home:%s' % uid, 0, -HOME_TIMELINE_SIZE-1)
    pipeline.execute()
    return True


def unfollow_user(conn, uid, other_uid):
    fkey1 = 'following:%s' % uid
    fkey2 = 'followers:%s' % other_uid

    if not conn.zscore(fkey1, other_uid):
        return None

    pipeline = conn.pipeline(True)
    pipeline.zrem(fkey1, other_uid)
    pipeline.zrem(fkey2, uid)
    pipeline.zcard(fkey1)
    pipeline.zcard(fkey2)
    pipeline.zrevrange('profile:%s' % other_uid,
                      0, HOME_TIMELINE_SIZE-1)
    following, followers, statuses = pipeline.execute()[-3:]
    pipeline.hset('user:%s' % uid, 'following', following)
    pipeline.hset('user:%s' % other_uid, 'followers', followers)
    if statuses:
        pipeline.zrem('home:%s' % uid, *statuses)
    pipeline.execute()
    clear_user_timeline(conn, uid, other_uid)
    return True

def clear_user_timeline(conn, uid, other_uid):
    msgformat = 'msg:uid:msgid'


