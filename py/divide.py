# encoding: utf-8
import itertools

def n_at_a_time(items, n):
    it = iter(items)
    return itertools.izip(*[it] * n)

li = range(1)
limit = 3

for i in n_at_a_time(li, 3):
    print i


def n_at_a_time(items, n):
    e = []
    for i in items:
        e.append(i)
        if len(e) % n == 0:
            yield e
            e = []
    if e:
        [e.append(None) for i in range(n - len(e))]
        yield e

for i in n_at_a_time(range(7), 3):
    print i


