# encoding: utf-8

import random
from datetime import datetime
import time

start = time.mktime(datetime(2011, 9, 9, 17).timetuple())
epoch_start = time.mktime(datetime(2011, 1, 1).timetuple())

custom_epoch = 1387263000 #  September 9th, 2011, at 5:00pm
print(start - epoch_start, custom_epoch)
print(datetime.fromtimestamp(custom_epoch))

def uid():
    # 16 bit
    # 13 ts | 3 randint
    ts = int(time.time() * 1000)
    return int('%s%03d' % (ts, random.randint(0, 10 ** 3)))

print(str(uid()), len(str(uid())))
