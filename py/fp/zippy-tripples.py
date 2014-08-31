import itertools

def prev_this_next(items):
    extend = itertools.chain([None], items, [None]) # makes a chain, start and ends with None
    prev, this, next = itertools.tee(extend, 3)
    try:
        this.next()
        next.next()
        next.next()
    except StopIteration:
        pass
    return itertools.izip(prev, this, next)

# Triples Times Two

def three_at_a_time(items):
    """
    >>> t = three_at_a_time((1, 2, 3, 4, 5, 6))
    >>> t.next()
    (1, 2, 3)
    >>> t.next()
    (4, 5, 6)
    >>> t.next()
    Traceback (most recent call last):
        ...
    StopIteration
    >>> ttt = three_at_a_time((1, 2, 3, 4))
    >>> [t for t in ttt]
    [(1, 2, 3)]
    >>> ttt = three_at_a_time(itertools.count())
    >>> ttt = itertools.islice(ttt, 0, 9, 3)
    >>> [t for t in ttt]
    [(0, 1, 2), (9, 10, 11), (18, 19, 20)]
    """

    it = iter(items)
    return itertools.izip(it, it, it)

def n_at_a_time(items, n):
    """
    >>> n_at_a_time((1, 2, 3, 4, 5, 6), 3)
    """
    it = iter(items)
    return itertools.izip(*([it] * n))

def test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    test()

