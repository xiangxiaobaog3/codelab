class Selector(object):

    def run(self):
        for c in self._children:
            if c.run():
                return True
        return False


class Sequence(object):
    def run(self):
        for c in self._children:
            if not c.run():
                return False
        return True
