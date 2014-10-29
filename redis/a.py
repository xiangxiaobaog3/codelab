# encoding: utf-8

import redis
import time

ONE_WEEK_IN_SECONDS = 7 * 86400
ARTICLES_PER_PAGE = 25
VOTE_SCORE = 86400 / 200

conn = redis.StrictRedis()

def post_article(conn, user, title, link):
    article_id = str(conn.incr('articles:'))
    voted = 'voted:' + article_id

    conn.sadd('voted:' + article_id, user)
    conn.expire(voted, ONE_WEEK_IN_SECONDS) # 一周后失效


    article = 'articles:' + article_id
    now = int(time.time())
    m = {
        "id": article_id,
        "title": title,
        "link": link,
        "poster": user,
        "time": now,
        "votes": 1,
        "down_votes": 1,
    }
    conn.zadd('time:', now, article)
    conn.zadd('score:', now + VOTE_SCORE, article_id)
    conn.hmset(article, m)
    return article


def article_vote(conn, user, article):
    cutoff = time.time() - ONE_WEEK_IN_SECONDS

    if conn.zscore('time:', article) < cutoff:
        return

    article_id = article.split(':')[-1]
    if conn.sadd('voted:' + article_id, user):
        pipeline = conn.pipeline()
        pipeline.zincrby('score:', article_id, VOTE_SCORE)
        pipeline.hincrby(article, 'votes', 1)
        print(pipeline.execute(), '---')


def article_down_vote(conn, user, article):
    # 降分 + 删除曾在 vote 组里的自己
    article_id = article.split(':')[-1]
    conn.srem('voted:' + article_id, user)
    conn.sadd('down_voted:' + article_id, user)
    conn.zincrby('score:', article_id, -VOTE_SCORE)
    # conn.smove('voted:' + article_id, 'down_voted:' + article_id, user)
    conn.hincrby(article, 'down_votes', 1)

def get_articles(conn, page, order='score:'):
    start = (page - 1) * ARTICLES_PER_PAGE
    end = start + ARTICLES_PER_PAGE - 1

    ids = conn.zrevrange(order, start, end)
    articles = []

    pipeline = conn.pipeline()

    for id in ids:
        pipeline.hgetall("articles:" + str(id))
    articles = pipeline.execute()
    return articles


# Grouping articles
def add_remove_groups(conn, article_id, to_add=[], to_remove=[]):

    # conn.hdel("articles:1", "groups")

    article = 'articles:' + article_id
    groups = conn.hget(article, "groups")
    if not groups:
        groups = set()
    else:
        groups = set(groups.split(","))

    for group in to_add:
        conn.sadd('group:' + group, article_id)
        groups.add(group)
    for group in to_remove:
        conn.srem('group:' + group, article_id)
        groups.discard(group)
    print(conn.hset(article, "groups", ",".join(groups)))


def get_group_articles(conn, group, page, order='score:'):
    key = order + group

    if not conn.exists(key):
        conn.zinterstore(key,
                        ['group:' + group, order],
                        aggregate='max')
        conn.expire(key, 60)

    return get_articles(conn, page, key)


def test():
    # post_article(conn, 'users:1', 'test page', 'test link')
    # post_article(conn, 'users:2', 'test page 2', 'test link 2')
    # post_article(conn, 'users:4', 'test page 3', 'test link 3')

    article_vote(conn, 'users:2', 'articles:1')
    article_vote(conn, 'users:3', 'articles:1')
    article_vote(conn, 'users:4', 'articles:2')
    article_vote(conn, 'users:5', 'articles:2')
    article_vote(conn, 'users:6', 'articles:2')
    article_down_vote(conn, 'users:6', 'articles:2')

    # add_remove_groups(conn, "1", ["test"])
    add_remove_groups(conn, "2", ["news"])

    print(get_articles(conn, 1))
    print(get_group_articles(conn, "news", 1))

test()
