from .bstree import BSTree, BSTNode


class RBTNode(BSTNode):

    __slots__ = ('_key', '_value', '_children',
                 '_height', '_parent', '__color',
                 '__left', '__right')

    def __init__(self, key, value, height,
                 parent, color, left=None, right=None):
        super(RBTNode, self).__init__(
            key, value, height, parent, left, right
        )

        self.__color = color

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color


class RBTree(BSTree):

    def __init__(self, root=None, iter_type=None):
        super(RBTree, self).__init__(root, iter_type)

    def __new_node(self, key, value, height, parent,
                   color, left, right):
        return RBTNode(key, value, height, parent,
                       color, left, right)

    def insert(self, key, value):
        pass

    def remove(self, key, value):
        pass
