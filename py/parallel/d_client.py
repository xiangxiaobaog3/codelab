from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
    pass


QueueManager.register("get_queue")

m = QueueManager(address=("127.0.0.1", 5000), authkey='_abc')

m.connect()
queue = m.get_queue()
queue.put("Hi there 11")
print([queue.get() for i in range(3)])

