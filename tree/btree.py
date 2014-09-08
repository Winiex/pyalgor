from .base import BaseNode, BaseTree


class BTNode(BaseNode):
    """Binary tree node."""

    def __init__(self, key, value,
                 left=None, right=None):
        children = [left, right]

        super(BTNode, self).__init__(
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

    def __setitem__(self, key, value):
        super(BTNode, self).__setitem__(key, value)

        if key == 0:
            self.left = value
        elif key == 1:
            self.right = value

    def __repr__(self):
        return '<BTNode: key %s, value %s>' % \
            (self.key, self.value)

    def free(self):
        super(BTNode, self).free()
        self.__left = None
        self.__right = None


class BinaryTree(BaseTree):

    def __init__(self, root=None):
        super(BinaryTree, self).__init__(root)

    def __new_node(self, key, value,
                   left=None, right=None):
        return BTNode(key, value,
                      left, right)

    def insert(self, key, value):
        if self.root is None:
            self.root = self.__new_node(key, value)
        else:
            parent = None
            direction = 0  # 0 means left, 1 means right.
            node = self.root
            while True:
                if node is None:
                    parent[direction] = self.__new_node(key, value)
                    break
                if key == node.key:
                    node.value = value
                    break
                else:
                    parent = node
                    direction = 0 if key <= node.key else 1
                    node = node[direction]

            self.count += 1

        return self

    def remove(self, key):
        node = self.root

        if node is None:
            raise KeyError('Tree is empty.')
        else:
            parent = None
            direction = 0
            while True:
                if key == node.key:
                    if node.left is not None and \
                       node.right is not None:
                        rep_parent = node
                        direction = 1
                        replacement = node[1]

                        while replacement.left is not None:
                            rep_parent = replacement
                            direction = 0
                            replacement = replacement[0]

                        rep_parent[direction] = replacement.right

                        if rep_parent != node:
                            rep_parent.left = None

                        node.key = replacement.key
                        node.value = replacement.value

                        replacement.free()
                    else:
                        down_direct = 1 if node.left is None else 0

                        if parent is None:
                            self.root = node[down_direct]
                        else:
                            parent[direction] = node[down_direct]

                        node.free()

                    self.count += -1
                    break
                else:
                    direction = 0 if key <= node.key else 1
                    parent = node
                    node = node[direction]

                    if node is None:
                        raise KeyError('Key not found.')
