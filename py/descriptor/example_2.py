#!/usr/bin/env python
# encoding: utf-8

from urlparse import urlparse
from datetime import datetime

now = datetime.now


class URLFieldProxy(unicode):
    @property
    def hostname(self):
        return urlparse(self).hostname


class ProxyFieldDescriptor(object):
    def __init__(self, field_name, proxy_class):
        self.field_name = field_name
        self.proxy_class = proxy_class

    def __get__(self, instance=None, owner=None):
        value = instance.__dict__[self.field_name]
        if value is None:
            return value
        return self.proxy_class(value)

    def __set__(self, instance, value):
        instance.__dict__[self.field_name] = value


class SomeObject(object):
    wormhole = ProxyFieldDescriptor('url', URLFieldProxy)

    def __init__(self, url):
        self.url = url


s = SomeObject('http://g.cn')
print(s.wormhole)
print(s.wormhole.hostname)


class TimestampedBooleanDescriptor(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, instance=None, owner=None):
        return instance.__dict__[self.name] is not None

    def __set__(self, instance, value):
        value = bool(value)
        if value != self.__get__(instance):
            if value:
                instance.__dict__[self.name] = now()
            else:
                instance.__dict__[self.name] = None


class SomeObject1(object):
    boolean = TimestampedBooleanDescriptor('timestamp')

    def __init__(self, timestamp=None):
        self.timestamp = timestamp


obj = SomeObject1()
obj.timestamp is None
print(obj.boolean)

obj.timestamp = now()
print(obj.boolean)
obj.boolean = False
print(obj.timestamp)
