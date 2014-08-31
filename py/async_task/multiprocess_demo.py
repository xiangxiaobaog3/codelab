#!/usr/bin/env python

import random
import string
import multiprocessing
from time import sleep


def is_queue_exhaust(task):
    return task is None


def do_something_with_task(process_name, task, q):
    t = random.random()
    sleep(t)
    print(process_name, task, t)
    q.put('done %s in %s seconds' % (task, t))


class WorkerProcess(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        super(WorkerProcess, self).__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        while True:
            task = self.task_queue.get()

            if is_queue_exhaust(task):
                self.task_queue.task_done()
                break

            do_something_with_task(self.name, task, self.result_queue)
            self.task_queue.task_done()


def main():
    task_queue = multiprocessing.JoinableQueue()
    result_queue = multiprocessing.Queue()
    process = 3
    workers = []

    for i in range(process):
        w = WorkerProcess(task_queue, result_queue)
        w.start()
        workers.append(w)

    for i in xrange(10):
        task_queue.put(''.join([random.choice(string.letters) for i in range(random.randint(1, 30))]))

    [task_queue.put(None) for i in range(process)]
    task_queue.join()

if __name__ == "__main__":
    main()
