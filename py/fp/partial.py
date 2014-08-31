import operator
from functools import partial

def log(level, message):
    print "[{level}]: {msg}".format(level=level, msg=message)

debug = partial(log, "debug")
debug("starting doing something")
debug("Continue with something else")

import math
def fsum(f):
    def apply(a, b):
        return sum(map(f, range(a, b+1)))
    return apply

log_sum = fsum(math.log)
square_sum = fsum(lambda x: x**2)
simple_sum = fsum(int)

print fsum(lambda x: x*2)(1, 10)
print fsum(partial(operator.mul, 2))(1, 10)


from operator import methodcaller
print methodcaller("__str__")([1, 2, 3, 4, 5])
print methodcaller("keys")(dict(name="Alexey", topic="FP"))

values_extractor = methodcaller("values")
print values_extractor(dict(name="Alexey", topic="FP"))
print methodcaller("count", 1)([1, 2, 3, 4])

ss = ["UA", "PyCon", "2012"]
print reduce(operator.add, map(len, ss))
