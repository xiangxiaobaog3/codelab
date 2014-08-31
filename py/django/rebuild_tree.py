from pprint import pprint
def rebuild_tree(node, lft):
    rgt = lft + 1
    print node.pop()
    for child in node:
        rgt = rebuild_tree(child, rgt)
    # node.lft, node.rgt = lft, rgt
    _rgt = rgt + 1
    print lft, _rgt
    return _rgt

tree = ['root',
        ['parent_1',
            ['child_1_1', 'child_1_2']],
        ['parent_2',
            ['child_2_1', 'child_2_2']]
    ]

pprint(tree)
rebuild_tree(tree, 0)
