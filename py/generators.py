def make_generator():
    """
    :returns: @todo

    """
    rv = yield 0
    print "got", rv
    rv = yield 1
    print "got", rv

g = make_generator()
i = g.send(None)
while True:
    try:
        print("i=", i)
        i = g.send(i + 10)
    except StopIteration:
        break
print("i=", i)
