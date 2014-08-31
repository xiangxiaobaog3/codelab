# encoding: utf-8

from multiprocessing import Queue
from multiprocessing.managers import BaseManager

queue = Queue()

class QueueManager(BaseManager):
    pass


QueueManager.register("get_queue", callable=lambda: queue)

m = QueueManager(address=("", 5000), authkey='_abc')

s = m.get_server()
s.serve_forever()
