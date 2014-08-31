expr, res = "28+32+++32++39", 0
for t in expr.split("+"):
    if t != "":
        res += int(t)

print res

from operator import add
expr = "28+32++32++39"

print reduce(add, map(int, filter(bool, expr.split("+"))))
print sum([int(i) for i in [j for j in expr.split('+') if j]])

# Mutable Dict + Partial binding

def ask(self, question):
    print "{name}, {q}?".format(name=self['name'], q=question)

def talk(self):
    print "I'm starting {topic}".format(topic=self['topic'])

from functools import partial

def cls(**methods):
    def bind(self):
        return lambda (name, method): (name, partial(method, self))
    return lambda **attrs: dict(
        attrs.items() + map(bind(attrs.copy()), methods.items())
    )


