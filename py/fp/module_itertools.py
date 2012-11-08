# MODULE "ITERTOOLS"
import itertools

print list(itertools.chain([1, 2, 3], [10, 20, 30]))
print list(itertools.chain(*(map(xrange, range(5)))))
print list(itertools.starmap(lambda k, v: "%s => %s" % (k, v),
                             {'a': 1, 'b': 2}.items()))
print list(itertools.imap(pow, (2, 3, 10), (5, 2, 3)))
print dict(itertools.izip("ABCD", [1, 2, 3, 4]))


