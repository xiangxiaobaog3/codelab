a = range(10)
print list(zip(a[:-1], a[1:]))

from itertools import izip_longest

x = range(7)
print list(izip_longest(*[iter(x)]*2))

print [(d.pop(0), d.pop(0)) for d in range(7)]
