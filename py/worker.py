# encoding: utf-8

from time import sleep
from threading import Thread
from Queue import Queue

class DispatcherThread(Thread):
    def __init__(self, *args, **kwargs):
        super(DispatcherThread, self).__init__(*args, **kwargs)
        self.interested_threads = []

    def run(self):
        while 1:
            # if some_condition:
            if True:
                some_message = 'dododo'
                self.dispatch_message(some_message)
            else:
                sleep(0.1)

    def register_interest(self, thread):
        self.interested_threads.append(thread)

    def dispatch_message(self, message):
        for thread in self.interested_threads:
            thread.put_message(message)


class WorkerThread(Thread):
    def __init__(self, *args, **kwargs):
        super(WorkerThread, self).__init__(*args, **kwargs)
        self.queue = Queue()

    def run(self):
        # tell the dispatcher thread we want messages
        dispatch_thread.register_interest(self)

        while 1:
            # Wait for next message
            message = self.queue.get()

            # Process message

    def put_message(self, message):
        self.queue.put(message)

dispatch_thread = DispatcherThread()
dispatch_thread.start()

worker_threads = []
for i in range(10):
    worker_thread = WorkerThread()
    worker_thread.start()
    worker_threads.append(worker_thread)

dispatch_thread.join()


