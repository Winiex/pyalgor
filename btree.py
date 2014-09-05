from .base import BaseNode, BaseTree


class BTNode(BaseNode):
    """Binary tree node."""

    def __init__(self, key, value,
                 left=None, right=None):
        children = []

        if left is not None:
            children[0] = left

        if right is not None:
            children[1] = right

        super(BTree).__init__(
            key, value, children
        )

        self.__left = left
        self.__right = right

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, left):
        self.__left = left

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, right):
        self.__right = right


class BTree(BaseTree):

    def __init__(self, data=None):
        pass

    @property
    def root(self):
        return self.__root

    def insert(self, key, value):
        pass

    def remove(self, key):
        pass
