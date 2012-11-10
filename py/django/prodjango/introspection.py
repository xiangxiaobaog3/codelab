#-*- encoding:utf-8 -*-

"""
~~~~~~~~~~~
python 内省
~~~~~~~~~~~

包含的一些元信息来描述自己

函数和类通常提供了以下一些属性用来标识它们

__name__: 定义的类和函数名称
__doc__: 定义的函数或类的 docstring
__module__ : 定义的函数或类的 import 路径
__class__ : 创建当前对象的类 (在python中，所有都是对象，对象是由类创建来的)

确定对象的类型 type
~~~~~~~~~~~~~~~~~~~~
报告一个异常的时候，包含异常的类型和它的值，在这些情况下，type被用来返回
类的对象，__name__ 属性能包含在日志里

检查特定的类型
~~~~~~~~~~~~~~
- issubclass(cls, base): 返回 cls 是否继承自 base
- isinstance(obj, base): 返回 obj 是否是 base 的实例或 base 是否是它的祖先

isinstance = issubclass(obj.__class__, SomeClasses)

函数特征
~~~~~~~~
inspect.getargspec(): 返回一个函数可接受的参数信息

- args: 一个包含函数所有接受的参数名的列表，如果函数不接受任何参数，
  这将是个空的列表
- varargs: 函数可接受的位置参数
- varkwargs: 函数可接受的关键字参数
- defaults: 包含函数可接受的默认参数值

docstring
~~~~~~~~~
inspect.getdoc()

"""

def test(a, b, c=True, d=False, *e, **f):
    pass

import inspect
print inspect.getargspec(test)


def get_defaults(func):
    args, varargs, varkwargs, defaults = inspect.getargspec(func)
    index = len(args)  - len(defaults) # Index of the first optional argument
    return dict(zip(args[index:], defaults))

print get_defaults(test)

def func(arg):
    """
    Performs a function on an argument and return the result.

    arg
        The argument to be processed
    """
    pass

print func.__doc__
print inspect.getdoc(func)
