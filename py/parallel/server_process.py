# encoding: utf-8

from multiprocessing import Manager, Process, current_process

def worker(alist):
    idx = int(current_process().name.split("-"))
    alist[idx-1] = (idx-1) **2


if __name__ == '__main__':
    n = 100
    manager = Manager()
    l = manager.list()
    l.extend(range(n))

    p = [Process(target=worker, args=(l, )) for i in range(n - 1)]

    for e in p:
        e.start()

    for e in p:
        e.join()

    print "Final result: ", l
