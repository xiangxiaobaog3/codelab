import time
import threading

import redis

def publisher(conn, n):
    time.sleep(1)
    for i in xrange(n):
        conn.publish('c1', i)
        time.sleep(1)


def run_pubsub(conn):
    threading.Thread(target=publisher, args=(conn, 3)).start()
    pubsub = conn.pubsub()
    pubsub.subscribe(['c1'])
    count = 0
    for item in pubsub.listen():
        print(item)
        count += 1
        if count == 4:
            pubsub.unsubscribe()
        if count == 5:
            break

conn = redis.Redis()
run_pubsub(conn)
