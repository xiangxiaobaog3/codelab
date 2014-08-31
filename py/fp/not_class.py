# ASSUME THAT WE DON'T HAVE DICT'
def dct(*items):
    def pair((key, value)):
        return lambda k: value if k == key else None
    def merge(l, r):
        return lambda k: l(k) or r(k)

    return reduce(merge, map(pair, items), pair((None, None)))

me = dct(("name", "alexey"), ("topic", "FP with Python"))
print me("name")
print me("topic")
