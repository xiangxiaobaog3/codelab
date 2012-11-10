#-*- encoding:utf-8 -*-

"""
装饰器
设计的原意是在函数执行前或后执行某部分代码
"""

def decorate(func):
    print 'Decorating %s...' % func.__name__
    def wrapped(*args, **kwargs):
        print 'Called wrapped function with args:', args
        return func(*args, **kwargs)

    print 'done'
    return wrapped

@decorate
def test(a, b):
    return a+b

test(1, 2)

"""
python2.5 引进了一个 partial 模块
"""
import functools
def add(a, b):
    return a + b
plus3 = functools.partial(add, 3)
print plus3(5)

# call the decorator with or without args

def decorate(func=None, prefix="Decorated"):
    def decorated(func):
        # this returns the final, decorated
        # function, regardless of how it was called
        def wrapper(*args, **kwargs):
            return '%s: %s' % (prefix, func(*args, **kwargs))
        return wrapper
    if func is None:
        # The decorator was called with arguments
        def decorator(func):
            return decorated(func)
        return decorator
    return decorated
