# encoding: utf-8

import functools

class DictProperty(object):

    """Property that maps to a key in a local dict-like attribute"""

    def __init__(self, attr, key=None, read_only=False):
        self.attr, self.key, self.read_only = attr, key, read_only

    def __call__(self, func):
        """

        :func: @todo
        :returns: @todo

        """
        functools.update_wrapper(self, func, updated=[])
        self.getter, self.key = func, self.key or func.__name__
        return self

    def __get__(self, obj, cls):
        """

        :obj: @todo
        :cls: @todo
        :returns: @todo

        """
        if obj is None: return self
        key, storage = self.key, getattr(obj, self.attr)
        if key not in storage: storage[key] = self.getter(obj)
        return storage[key]

    def __set__(self, obj, value):
        if self.read_only:
            raise AttributeError("Read-Only property.")
        getattr(obj, self.attr)[self.key] = value

    def __delete__(self, obj):
        if self.read_only:
            raise AttributeError("Read-Only property.")
        del getattr(obj, self.attr)[self.key]


d = DictProperty('config', 'catchall')
print dir(d)
