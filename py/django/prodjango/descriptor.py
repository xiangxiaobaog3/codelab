#-*- encoding:utf-8 -*-

import datetime

class CurrentDate(object):
    def __get__(self, instance, owner):
        return datetime.date.today()
    def __set__(self, instance, value):
        raise NotImplementedError("can't change the current date.")

class Example(object):
    date = CurrentDate()

e = Example()
print e.date.day
print e.date
# e.date = datetime.date.today()

class Descriptor(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

class BaseModel(object):
    pass

class DateTimeModel(BaseModel):
    pass

class DateTimeType(type):
    def __new__(cls, name, parents, dct):
        attrs = ((name, value) for name, value in dct.items()
                  if not name.startswith('__'))
        attrs = dict(attrs)
        for name, value in attrs.items():
            if isinstance(value, DateTimeModel):
                attrs[name] = Descriptor(name)
        return type.__new__(cls, name, parents, attrs)

class TestObject(object):
    attr = DateTimeModel()
    __metaclass__ = DateTimeType

test = TestObject()
test.attr = 6
print test.attr
