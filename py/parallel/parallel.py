# encoding: utf-8

from multiprocessing import Process, Queue, Lock


def say_hello(name='world', **kwargs):
    """@todo: Docstring for say_hello
    """
    l = Lock()
    l.acquire()
    print "Hello, %s" % name, kwargs
    l.release()


if __name__ == '__main__':
    p = Process(target=say_hello, args=('Danll', ), kwargs={"xx": "xx"})
    p.start()
    print p.pid

    p.join()

    q = Queue()
    q.put("When hello there!")
    q.put(["a", 1, {"b": "c"}])

    print(q.get())
    print(q.get())

