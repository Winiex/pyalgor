from .exception import AppendModeException
from .tree import Tree, TNode
from .iters import DFIter, BFIter, PreOrderIter, InOrderIter, PostOrderIter


class BTNode(TNode):
    """
    Binary tree node.
    """
    __slots__ = ('_key', '_value', '_children',
                 '_height', '_parent', '_left', '_right')

    def __init__(self, key, value, height,
                 parent, left=None, right=None):
        children = [left, right]

        super(BTNode, self).__init__(
            key, value, height, parent, children
        )

        self._left = left
        self._right = right

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, left):
        self._left = left
        self._children[0] = left

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, right):
        self._right = right
        self._children[1] = right

    @property
    def side_of_parent(self):
        """
        Judge which side of its parent is the node on.

        On the left return 0, on the right return 1.
        If the node has no parent, the method returns -1.
        """
        if self._node_empty(self._parent):
            return -1

        if self._parent.left is self:
            return 0
        elif self._parent.right is self:
            return 1
        else:
            raise ValueError('Node invalid.')

    def __setitem__(self, key, value):
        super(BTNode, self).__setitem__(key, value)

        if key == 0:
            self._left = value
        elif key == 1:
            self._right = value

    def __repr__(self):
        return '<BTNode: key %s, value %s>' % \
            (self._key, self._value)

    def free(self):
        super(BTNode, self).free()
        self._left = None
        self._right = None


class BinaryTree(Tree):
    """
    Binary tree.
    """
    _accept_iters = (DFIter, BFIter, PreOrderIter,
                     InOrderIter, PostOrderIter)

    def __init__(self, root=None, iter_type=None, append_mode=False):
        super(BinaryTree, self).__init__(root, iter_type)
        self._append_mode = append_mode

    def __new_node(self, key, value, height, parent,
                   left=None, right=None):
        return BTNode(key, value, height, parent,
                      left, right)

    def insert(self, parent_key, key, value):
        if self._append_mode:
            raise AppendModeException('BinaryTree in append mode.')
        return self

    def append(self, key, value):
        if not self._append_mode:
            raise AppendModeException('BinaryTree must be in append mode.')
        return self

    def replace(self, replace_key, key, value):
        return self

    def remove(self, key):
        pass
