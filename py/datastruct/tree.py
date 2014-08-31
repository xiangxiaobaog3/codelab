#-*- encoding:utf8 -*-

class Node(object):
    def __init__(self, value, children=[]):
        self.value = value
        self.children = children

    def __repr__(self, level=0):
        indent = ' ' * 4
        ret = ret = indent * level + repr(self.value) + "\n"
        for child in self.children:
            ret += child.__repr__(level+1)
        return ret


tree = Node("grandmother", [
    Node("daugther", [
        Node("granddaugher"),
        Node("grandson"),
    ]),
    Node("son", [
        Node("granddaugher"),
        Node("grandson"),
    ]),
])

print(tree)


class exprnode(object):
    """Expression tree"""
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def evaluate(self):
        if self.value == '+':
            return self.left.evaluate() + self.right.evaluate()
        elif self.value == '-':
            return self.left.evaluate() - self.right.evaluate()
        elif self.value == '*':
            return self.left.evaluate() * self.right.evaluate()
        elif self.value == '/':
            return self.left.evaluate() / self.right.evaluate()
        else:
            return self.value

my_expr = exprnode('*',
    exprnode('+', exprnode(2), exprnode(3)),
    exprnode(4)
)
print(my_expr.evaluate())


class binarynode(object):
    """平衡二叉树"""
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def search(self, value):
        # return True if value is in the tree
        if self.value == value:
            return True
        if value < self.value:
            if self.left != None:
                return self.left.search(value)
            return False
        else:
            if self.right != None:
                return self.right.search(value)
            return False

    def insert(self, item):
        if self.value == item:
            return # 不允许有相同的值出现
        if item < self.value: # 插左边
            if self.left != None:
                self.left.insert(item)
            else:
                self.left = binarynode(item)
        else: # 插右边
            if self.right != None:
                self.right.insert(item)
            else:
                self.right = binarynode(item)

    def delete(self, value):
        if value == self.value:
            if self.left != None:
                self.value = self.left.highest()
                self.left.delete(self.value)
            elif self.right != None:
                self.value = self.right.lowest()
                self.right.delete(self.value)
            else:
                return None
        else:
            if value < self.value and self.left != None:
                self.left = self.left.delete(value)
            if value > self.value and self.right != None:
                self.right = self.right.delete(value)
            return self

    def highest(self):
        if self.right:
            return self.right.highest()
        return self.value

    def lowest(self):
        if self.left:
            return self.left.lowest()
        return self.value

btree = binarynode(4)
[btree.insert(i) for i in [2, 6, 1, 5, 7, 3]]
print(btree.search(2))
