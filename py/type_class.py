#!/usr/bin/env python
# encoding: utf-8
# copyleft


class X(object):
    a = 1


# type(name, bases, dict) -- create a new type object
x = type('X', (object, ), dict(a=1))
print(x.a)


# __new__ is first step instance creation, returing a new instance of
# your class
# __new__(cls, name, )

class SubFieldBase(type):

    """保证类属性有描述器协议"""

    def __new__(cls, name, bases, attrs):
        new_class = super(SubFieldBase, cls).__new__(name, bases, attrs)
        new_class.contribute_to_class = make_contrib(
            new_class, attrs.get('contribute_to_class')
        )
        return new_class


class Creator(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)

def make_contrib(superclass, func=None):
    def contribute_to_class(self, cls, name):
        if func:
            func(self, cls, name)
        else:
            super(superclass, self).contribute_to_class(cls, name)
        setattr(cls, self.name, Creator(self))
    return contribute_to_class


class Field(object):
    __metaclass__ = SubFieldBase
    a = 1

    def to_python(self, value):
        return "| {0} |".format(value)


f = Field()
print f

