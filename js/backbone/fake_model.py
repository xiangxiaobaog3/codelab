# encoding: utf-8

class Dispatcher(object):
    def __init__(self):
        self.events = {}

    def add_listener(self, event, func):
        if event not in self.events:
            self.events[event] = set()
        self.events[event].add(func)

    def dispatch(self, event, *args, **kwargs):
        for func in self.events.get(event, []):
            func(*args, **kwargs)


def on_change(model, key, value):
    print(model, key, 'attribute changed')


class Model(object):

    def __init__(self):
        self.dispatcher = Dispatcher()
        self.dispatcher.add_listener('change', on_change)

    def set(self, key, value):
        setattr(self, key, value)
        self.dispatcher.dispatch('change', self, key, value)
        self.dispatcher.dispatch('change:' + key, self, key, value)

    def on(self, event, func):
        self.dispatcher.add_listener(event, func)


def on_title_changed(model, key, value):
    print("title changed")


m = Model()
m.set('a', 'b')
m.on('change:title', on_title_changed)
m.set('title', 'ffff')
