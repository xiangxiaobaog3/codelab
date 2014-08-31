from multiprocessing import Process, Queue, Lock

def say_hello(name='world'):
    print "Hello, %s" % name

p = Process(target=say_hello)
p.start()
p.join() # complete this process


q = Queue()

q.put('Why hello')
q.put(['a', 1, {'b': 'c'}])
print q.get()
print q.get()

l = Lock()

l.acquire()
print 'Ha! Only I can write to stdout!'
l.release()
