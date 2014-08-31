# encoding: utf-8

import time

def coroutine(func):
    def _w(*args, **kws):
        cr = func(*args, **kws)
        cr.next()
        return cr
    return _w

def follow(thefile, target):
    thefile.seek(0, 2) # goto the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        target.send(line)


@coroutine
def printer():
    while True:
        line = (yield)
        print line,

f = open('a.txt')
follow(f, printer())
