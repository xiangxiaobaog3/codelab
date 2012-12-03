"""
Thread Local Storage
Per-thread data
"""

import threading

L = threading.local()

print 'in main thread, setting zop to 42'

L.zop = 42

def targ():
    print 'in subthread, setting zop to 23'
    L.zop = 23
    print 'in subthread, zop is now', L.zop

t = threading.Thread(target=targ)
t.start()
t.join()

print 'in main thread, zop is now', L.zop
