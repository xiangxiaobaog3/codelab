class Tree:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


# In-order lazy iterator (aka generator)
def inorder(tree):
    if tree is not None:
        for x in inorder(tree.left):
            yield x
        yield tree.data
        for x in inorder(tree.right):
            yield x

# Reverse in-order lazy iterator
def rev_inorder(tree):
    if tree is not None:
        for x in rev_inorder(tree.right):
            yield x
        yield tree.data
        for x in rev_inorder(tree.left):
            yield x

n1 = Tree(1)
n2 = Tree(2)
n3 = Tree(3)
n4 = Tree(4)
n5 = Tree(5, n1, n2)
n6 = Tree(6, n3, n4)
n7 = Tree(7, n5, n6)

for i in inorder(n7):
    print i,
print

for i in rev_inorder(n7):
    print i,
print
