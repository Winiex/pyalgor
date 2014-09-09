from .bstree import BSTNode, BSTree


class AVLNode(BSTNode):
    __slots__ = ('_children', '_key', '_value', '_balance',
                 '__left', '__right')

    def __init__(self, key, value,
                 left=None, right=None):
        super(AVLNode, self).__init__(
            key, value, left, right
        )

        self.balance = 0


class AVLTree(BSTree):
    """Adelson-Velskii and Landis' tree, namely,
    self-balancing binary search tree."""
    def __init__(self, key, value,
                 left=None, right=None):
        super(AVLTree, self).__init__(
            key, value, left, right
        )

    def _new_node(self, key, value):
        return AVLNode(key, value)

    def insert(self, key, value):
        pass

    def remove(self, key):
        pass

    def search(self, key):
        pass
