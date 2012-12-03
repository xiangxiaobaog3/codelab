#-*- encoding:utf-8 -*-

"""
The observer pattern (sometimes known as publish/subscribe) is a
design pattern used in computer programming to observe the state of
an object in a program.
"""

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def scale(self, n):
        self.x = n * self.x
        self.y = n * self.y

def notify(f):
    def g(self, n):
        print 'scale', n
        return f(self, n)
    return g

Point.scale = notify(Point.scale)
p = Point(2.0, 3.0)
p.scale(2.5)
