#-*- encoding:utf-8 -*-
"""
Q: 什么是__metaclass__?
A:
"""

class SubclassTracker(type):
    def __init__(cls, name, bases, attrs):
        try:
            if TrackedClass not in bases:
                return
        except NameError:
            return
        cls._registry.append(cls)

class TrackedClass(object):
    __metaclass__ = SubclassTracker
    _registry = []

class ClassOne(TrackedClass):
    pass

print TrackedClass._registry

class ClassTwo(TrackedClass):
    pass

print TrackedClass._registry
