from .bstree import BSTNode, BSTree


class AVLNode(BSTNode):
    __slots__ = ('_children', '_key', '_value', '_balance',
                 '__left', '__right')

    def __init__(self, key, value, balance,
                 left=None, right=None):
        super(AVLNode, self).__init__(
            key, value, left, right
        )


class AVLTree(BSTree):
    """Adelson-Velskii and Landis' tree, namely,
    self-balancing binary search tree."""
