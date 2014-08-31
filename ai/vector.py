# encoding: utf-8

import math


class Vector2(object):
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "<Vector (%s, %s)>" % (self.x, self.y)

    def __add__(self, b):
        return Vector2(self.x + b.x, self.y + b.y)

    def __sub__(self, b):
        return Vector2(self.x - b.x, self.y - b.y)

    def __mul__(self, b):
        return self.x * b.x + self.y * b.y

    def __len__(self):
        return self.length

    def length_sq(self):
        # 返回矢量的平方
        return self.x**2 + self.y**2

    def length(self):
        return math.sqrt(self.length_sq())

    def normalize(self):
        # 归一化
        l = self.length()
        return Vector2(self.x/l, self.y/l)

    def dot(self, b):
        return math.acos(self.normalize() * b.normalize())

    def is_zero(self):
        return self.x == 0 and self.y == 0

    def sign(self, b):
        pass


v1 = Vector2(1, 0)
v2 = Vector2(4, 5)

print(v1 + v2)
print(v1 - v2)
print(v2.normalize())
print(v1.dot(v2))
