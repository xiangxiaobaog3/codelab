add = lambda a, b: a+b

def calculations(a, b):
    def add():
        return a + b
    return a, b, add

print calculations(1, 20)

# Pass function as argument
print map(lambda x: x^2, [1, 2, 3, 4, 5])

from time import time
# function returns function
def speak(topic):
    print 'my speach is', topic

def timer(fn):
    def inner(*args, **kwargs):
        t = time()
        fn(*args, **kwargs)
        print 'took {time}'.format(time=time() - t)
    return inner

speaker = timer(speak)
print speaker('xxxx')

