class A(object):
    def a(self):
        print "AAAA"

class B(object):
    def a(self):
        print "BBBBB"


class C(A, B):
    pass


c = C()
c.a()
print C.__mro__
