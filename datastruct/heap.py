class Heap(object):

    """Binary Heap implemention"""

    def __init__(self, size):
        self.num = 0
        self.size = size
        self.data = [None] * size

    def __repr__(self):
        return '<Heap: %s>' % (self.data,)

    def insert(self, x):
        if self.num >= self.size:
            return -1

        self.num += 1
        i = self.num
        self.data[i] = x
        while i > 0:
            j = i >> 1
            if self.data[i] > self.data[j]:
                t = self.data[i]
                self.data[i] = self.data[j]
                self.data[j] = t
            else:
                break
            i = j
        return 0

    def left_child_idx(self, i):
        return ((i + 1) << 1) - 1

    def right_child_idx(self, i):
        return (((i+1) << 1) + 1) - 1

    def check(self):
        i = 0
        while self.right_child_idx(i) < self.num:
            assert less_or_equal(self.data[self.left_child_idx[i]], self.data[i]), i
            assert less_or_equal(self.data[self.right_child_idx[i]], self.data[i]), i
            i = i == 0 and 1 or i << 1

def less_or_equal(a, b):
    if a is None or b is None:
        return True
    return a <= b

def build(ls):
    pass
