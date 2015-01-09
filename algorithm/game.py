#!/usr/bin/env python
# encoding: utf-8


class Stack(object):

    def __init__(self, elements=None):
        if elements is not None:
            self.elements = elements
        else:
            self.elements = []

    def push(self, el):
        self.elements.append(el)

    def pop(self):
        return self.elements.pop()

    def pop_elements_by_idx(self, idx):
        li = self.elements[idx:]
        self.elements = self.elements[:idx]
        return li

    def pop_elements_by_element(self, element):
        idx = self.index(element)
        li = []
        if idx is not None:
            li = self.pop_elements_by_idx(idx)
        return li

    def index(self, el):
        if el in self.elements:
            return self.elements.index(el)
        else:
            return None

    def is_empty(self):
        return len(self.elements) == 0


def game():
    p1 = Stack([2, 4, 1, 2, 5, 6])
    p2 = Stack([3, 1, 3, 5, 6, 4])

    plat = Stack()

    while True:
        c1 = p1.pop()
        if plat.index(c1):
            elements = plat.pop_elements_by_element(c1)
            p1.elements += elements + [c1]
        else:
            plat.push(c1)

        c2 = p2.pop()

        if plat.index(c2):
            elements = plat.pop_elements_by_element(c2)
            p2.elements += elements + [c2]
        else:
            plat.push(c2)

        print('plat -->', plat.elements)
        if p1.is_empty() or p2.is_empty():
            print(p1.elements, p2.elements)
            break

def main():
    game()

if __name__ == '__main__':
    main()
