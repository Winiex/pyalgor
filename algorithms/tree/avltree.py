from .bstree import BSTNode, BSTree


class AVLTNode(BSTNode):
    __slots__ = ('_children', '_key', '_value', '_balance',
                 '_left', '_right')

    def __init__(self, key, value,
                 left=None, right=None):
        super(AVLTNode, self).__init__(
            key, value, left, right
        )

        self.balance = 0


class AVLTree(BSTree):
    """
    Adelson-Velskii and Landis' tree, namely,
    self-balancing binary search tree.
    """
    def __init__(self, root=None, iter_type=None, append_mode=False):
        super(AVLTree, self).__init__(root, iter_type, append_mode)

    def _new_node(self, key, value):
        return AVLTNode(key, value)

    def insert(self, key, value):
        pass

    def remove(self, key):
        pass

    def search(self, key):
        pass
