# encoding: utf-8

import gevent
from gevent import Greenlet


def foo(message, n):
    gevent.sleep(n)
    print(message)


class MyGreenlet(Greenlet):

    def __init__(self, message, n):
        Greenlet.__init__(self)
        self.message = message
        self.n = n

    def _run(self):
        print(self.message)
        gevent.sleep(self.n)


g = MyGreenlet("hi there!", 3)
g.start()
g.join()

t1 = Greenlet.spawn(foo, "hello", 1)
t2 = gevent.spawn(foo, "I live", 2)
t3 = gevent.spawn(lambda x: x+1, 2)
threads = [t1, t2, t3]
gevent.joinall(threads)
