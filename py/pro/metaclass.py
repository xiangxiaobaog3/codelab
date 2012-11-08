#-*- encoding:utf-8 -*-

"""
metaclass:
- 参与类的创建
- 修改类
- 返回修改的类

Class as objects

在多数情况下类就是一堆生成对象的代码
但在python里，类也是对象
这个对象（类）能够创建对象（实例化），这就是为什么它被叫做类
既然它是一个对象，那么你可以
- 给它分配一个变量
- 你能拷贝它
- 你能为它增加属性
- 你能把它作为一个函数的参数传递

"""
class ObjectCreator(object): # 在内存里创建一个叫 ObjectCreator 的对象
    pass

def echo(o):
    print o

# 实例化
my_obj = ObjectCreator()
# 作为函数参数传递
echo(my_obj)
# 调用属性
print hasattr(ObjectCreator, 'new_attribute')
# 设置属性
ObjectCreator.new_attribute = 'foo'
print hasattr(ObjectCreator, 'new_attribute')
# 分配一个变量存储
ObjectCreatorMirror = ObjectCreator
print ObjectCreatorMirror

"""
动态创建类

因为类也是对象，所以你可以像对象一样在运行时创建
"""
def choose_class(name):
    if name == 'foo':
        class Foo(object):
            pass
        return Foo
    else:
        class Bar(object):
            pass
        return Bar
MyClass = choose_class('foo')
print MyClass
print MyClass()

"""
因为类也是对象，所以它们也是靠其它的什么来生成的
当你使用关键字 class ，python 会自动帮你创建这类对象
但在python里，你可以手动去创建一个这样的对象

"""

# 让我们用 type 函数看看对象的类型是什么
print type(1)
print type("1")
print type(ObjectCreator)
print type(ObjectCreator())

"""
当然， type 有一个完全不同的功能，
type can take the description of a class as parameters, and return a class

type works this way:

    type(name of the class,
         tuple of the parent class (for inheritance, can be empty),
         dictionary containing attributes names and values)

"""

MyShinyClass = type('MyShinyClass', (), {}) # 结果是生成一个类对象
print MyShinyClass
print MyShinyClass() # 实例化对象

"""
type 接受一个字典用来定义它的类的属性
"""
class Foo(object):
    bar = True
print Foo.bar
# 等价于
Foo = type('Foo', (), {'bar': True})
print Foo.bar

# 当然，你可以继承它
class FooChild(Foo):
    pass
# 同样等于
FooChild = type('FooChild', (Foo, ), {})
print FooChild
print FooChild.bar

# 最后，你想要增加一些方法到你的类里，just define a function with proper
# signature and assign it as an attribute
def echo_bar(self):
    print self.bar

FooChild = type('FooChild', (Foo, ), {'echo_bar': echo_bar})
print hasattr(FooChild, 'echo_bar')
FooChild().echo_bar()

"""
You see where we are going: in Python, classes are objects, and you can
create a class on the fly, dynamically.

This is what Python does when you use the keyword class, and it does so
by using a metaclass
"""

"""
神马是 元类 metaclasses
metaclasses 就是创建 classess 的东西, 用来创建类对象的类

MyClass = MetaClass()
MyObject = MyClass()

type 就是一个元类， type 就是 python 用来创建所有类的元类
在python里，所有的元素都是对象，包括整数，字符，函数和类，并且他们都是从
一个类创建而来的
"""
age = 35
print age.__class__
name = 'bob'
print name.__class__
def foo(): pass
print foo.__class__
class Bar(object): pass
b = Bar()
print b.__class__

# 那么 __class__ 的 __class__ 是什么呢？
print age.__class__.__class__
print name.__class__.__class__
print foo.__class__.__class__
print b.__class__.__class__

"""
所以 type 就是python内建的元类，当然，你也可以创建你自己的元类

__metaclass__ 属性
你可以在创建一个类的时候增加一个 __metaclass__ 属性

class Foo(object):
    __metaclass__ = something ...
    [....]

如果你这样做， python 就会使用叫 something 的元类来创建 Foo 类
你写了一个 class Foo(object)  首先，类对象 Foo 不会马上在内存创建的
python 会先选找类定义里是否有 __metaclass__ 属性，如果它找到了，它会
先使用它来创建对象类，如果没有，那么就就会使用 type 来创建类

当你这样做的时候

class Foo(Bar):
    pass

python 会干以下的事情:
1. 在 Foo 是否有一个叫 __metaclass__ 的属性？
2. 如果有，使用 __metaclass__ 在内存里创建一个叫 Foo 的类对象
3. 如果 python 找不到 __metaclass__, 它会去 Bar （父类）里去找 __metaclass__, 然后做跟 1， 2相同的事情
4. 如果 python 在父类里仍然找不到任何 __metaclass__ ，它会再去模块层找
   __metaclass__, 然后再做1，2 相同的事情
5. 最后它还是没有找到的话，它就会使用 type 来创建类对象

所以最大的问题是，你要把 __metaclass__ 放到哪里？
答案就是： 你要创建类的地方
什么创建类呢？ type ， 或者其它子类化的对象

元类的最大用处是当你创建类时自动改变类
通常用在API，
"""

"""
最简单的一个用例
当你需要一个类，这个类的所有属性都必须是大写
"""

def upper_attr(future_class_name, future_class_parents, future_class_attr):
    """
    Return a class object, with the list of its attribute turned
    into uppercase.
    """
    # pick up any attribute that doesn't start with '__'
    attrs = ((name, value) for name, value in future_class_attr.items()
             if not name.startswith('__'))
    uppercase_attr = dict((name.upper(), value) for name, value in attrs)

    # let `type` do the class creation
    return type(future_class_name, future_class_parents, uppercase_attr)

__metaclass__ = upper_attr

class Foo(): # 全局的__metaclass__不会与 object工作
             # 但是我们可以在这里定义 __metaclass__ 只让当前这个类收到影响
             #
    bar = 'bip'

print hasattr(Foo, 'bar')
print hasattr(Foo, 'BAR')

f = Foo()
print f.BAR

# 记住 `type` 也是类， 跟 `str` 和 `int` 一样
# 所以你可以继承它

class UpperAttrMetaclass(type):
    # __new__ is the method called before __init__
    # it's the method that creates object and returns it
    # __new__ 在 __init__ 调用前调用，它是用来创建返回对象的
    # 而__init__ 是用来初始化对象的
    # 你几乎很少会用到 __new__ ,除非当你想要控制对象是怎么被创建的

    def __new__(upperattr_metaclass, future_class_name,
                future_class_parents, future_class_attr):
        attrs = ((name, value) for name, value in future_class_attr.items()
                 if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        # 非OOP的写法
        # return type(future_class_name, future_class_parents, uppercase_attr)
        # 直接使用 type 这样我们就不用覆盖父类的 __new__ 方法了
        # upperattr_metaclass, 方法永远都接受来自当前实例作为第一个参数
        # 就跟 self 一样
        return type.__new__(upperattr_metaclass,
                            future_class_name,
                            future_class_parents,
                            uppercase_attr)

class UpperAttrMetaclassSimple(type):
    def __new__(cls, name, bases, dct):
        attrs = ((name, value) for name, value in dct.items()
                 if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        return type.__new__(cls, name, bases, uppercase_attr)

"""
Why would you use metaclasses classes instead of functions?
Since __metaclass__ can accept any callable, why would you use a class since it's obviously more complicated?

There are several reasons to do so:

The intention is clear. When you read UpperAttrMetaclass(type), you know what's going to follow
You can use OOP. Metaclass can inherit from metaclass, override parent methods. Metaclasses can even use metaclasses.
You can structure your code better. You never use metaclasses for something as trivial as the above example. It's usually for something complicated. Having the ability to make several methods and group them in one class is very useful to make the code easier to read.
You can hook on __new__, __init__ and __call__. Which will allow you to do different stuff. Even if usually you can do it all in __new__, some people are just more comfortable using __init__.
These are called metaclasses, damn it! It must mean something!'
"""
