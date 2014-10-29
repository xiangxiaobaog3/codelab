# encoding: utf-8

ARTICLES_PER_PAGE = 25


def get_articels(conn, page, order='score'):
    # id包含时间为key
    # 可以取出一天的所包含的对象
    start = (page - 1) * ARTICLES_PER_PAGE
    end = start + ARTICLES_PER_PAGE - 1

    ids = conn.zrevrange(order, start, end)
    articles = []
    for _id in ids:
        article_data = conn.hgetall(_id)
        article_data['id'] = id
        articles.append(article_data)
    return articles

def add_remove_groups(conn, article_id, to_add=[], to_remove=[]):
    article = 'article:' + article_id
    for group in to_add:
        conn.sadd('group:' + group, article)
    for group in to_remove:
        conn.srem('group:' + group, article)


def get_group_articles(conn, group, page, order='score:'):
    key = order + group
    if not conn.exists(key):
        # 如果不存在key，创建二个集合的交集排序集合
        conn.zinterstore(key,
                        ['group:' + group, order],
                        aggregate='max')
        conn.expire(key, 60) # 60 秒后失效

