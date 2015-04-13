#!/usr/bin/env python
# encoding: utf-8


"""

Abstract
--------

`__get__()`
`__set__()`
`__delete__()`
如果有以上方法在对象上被定义了， 这个对象就可以被称为一个描述器


Descriptor Protocol
-------------------
`descr.__get__(self, obj, type=None) ---> value`
`descr.__set__(self, obj, value)     ---> None`
`descr.__delete__(self, obj)         ---> None`

定义一个只读数据的描述器， 只需要定义 `__get__()` 和 一个调用会触发
`AttributeError`异常的 `__set__()` 方法即可。


Invoking Descriptors
--------------------
一个描述器能直接被它的方法名调用， 如`d.__get__(obj)`

对于对象来说，调用 `object.__getattribute__()` 会将 `b.x` 转化为`type(b).__dict__['x].__get__(b, type(b))'`

- 描述器是被`__getattribute__()`方法调用的
- 覆写 `__getattribute__()` 阻止了自动的描述器方法调用

"""


class RevealAccess(object):
    """
    A data descriptor that sets and returns values
    normally and prints a message logging their access.
    """

    def __init__(self, intval=None, name='val'):
        self.val = intval
        self.name = name

    def __get__(self, obj, objtype):
        print("Retrieving", self.name)
        return self.val

    def __set__(self, obj, val):
        print("Updating", self.name, obj, val)
        self.val = val

class MyClass(object):
    x = RevealAccess(10, 'var x')
    y = 5


m = MyClass()
m.x
m.x = 20
