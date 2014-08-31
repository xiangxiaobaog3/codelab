# encoding: utf-8

class cached_property(object):
    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        print("__get__", obj, cls)
        if obj is None: return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


class A(object):

    @cached_property
    def call(self):
        return "A"


a = A()
print(a.call)
print(a.call)
