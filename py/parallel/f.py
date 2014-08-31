# encoding: utf-8

from multiprocessing import Queue, Process, current_process


def worker(tasks, results):
    t = tasks.get()
    result = t * 2

    results.put([current_process().name, t, "*", 20, "=", result])


if __name__ == '__main__':
    n = 100
    my_tasks = Queue()
    my_results = Queue()

    workers = [Process(target=worker, args=(my_tasks, my_results))
               for i in range(n)]

    for each in workers:
        each.start()


    for each in range(n):
        my_tasks.put(each)

    while n:
        result = my_results.get()
        print "Res: ", result
        n -= 1
