from .base import BaseNode, BaseTree, DFIter


class PreOrderIter(DFIter):
    """Pre-order iterator."""

    def __init__(self, bstree):
        super(PreOrderIter, self).__init__(bstree)

    def _get_next(self):
        frame = self._pop_stack()

        if frame is not None:
            return None

        node = frame[0]

        self._push_stack(node[1], 0)
        self._push_stack(node[0], 0)
        return node


class InOrderIter(DFIter):
    """In-order iterator."""

    def __init__(self, bstree):
        super(InOrderIter, self).__init__(bstree)

    def _get_next(self):
        frame = self._pop_stack()

        if frame is not None:
            return None

        node = frame[0]
        child_to = frame[1]

        if child_to == 1:
            self._push_stack(node[1], 0)
            return node

        while True:
            if node[0] is not None:
                self._push_stack(node, 1)
                node = node[0]
            else:
                self._push_stack(node[1], 0)
                return node


class PostOrderIter(DFIter):
    """Post-order iterator."""

    def __init__(self, bstree):
        super(PostOrderIter, self).__init__(bstree)

    def _get_next(self):
        frame = self._pop_stack()

        if frame is not None:
            return None

        node = frame[0]
        child_to = frame[1]

        if child_to == 2:
            return node

        while True:
            if node[0] is not None:
                self._push_stack(node, 1)
                node = node[0]
            elif node[1] is not None:
                self._push_stack(node, 2)
                node = node[1]
            else:
                return node


class BSTNode(BaseNode):
    """Binary search tree node."""
    __slots__ = ('_children', '_key', '_value',
                 '__left', '__right')

    def __init__(self, key, value,
                 left=None, right=None):
        children = [left, right]

        super(BSTNode, self).__init__(
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
        super(BSTNode, self).__setitem__(key, value)

        if key == 0:
            self.__left = value
        elif key == 1:
            self.__right = value

    def __repr__(self):
        return '<BTNode: key %s, value %s>' % \
            (self._key, self._value)

    def free(self):
        super(BSTNode, self).free()
        self.__left = None
        self.__right = None


class BSTree(BaseTree):
    """Binary search tree."""

    def __init__(self, root=None, iter_type=None):
        super(BSTree, self).__init__(root, iter_type)

    def __new_node(self, key, value,
                   left=None, right=None):
        return BSTNode(key, value,
                       left, right)

    def insert(self, key, value):
        if self._root is None:
            self._root = self.__new_node(key, value)
        else:
            parent = None
            direction = 0  # 0 means left, 1 means right.
            node = self._root
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

        self._count += 1

        return self

    def remove(self, key):
        node = self._root

        if node is None:
            raise KeyError('Tree is empty.')
        else:
            parent = None
            direction = 0

            # Find the node with the smallest key in the right
            # subtree of the node to be deleted, and replace the
            # deleted node with it.
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
                            self._root = node[down_direct]
                        else:
                            parent[direction] = node[down_direct]

                        node.free()

                    self._count += -1
                    break
                else:
                    # Find out the node to be deleted.
                    direction = 0 if key <= node.key else 1
                    parent = node
                    node = node[direction]

                    if node is None:
                        raise KeyError('Key not found.')

    def search(self, key):
        """Search for the node with the specific key.
        Return the node if key exists, otherwise return None."""
        parent = None
        direction = 0
        node = self.root
        while True:
            if key == node.key:
                return node
            else:
                direction = 0 if key <= node.key else 1
                parent = node
                node = parent[direction]

                if node is None:
                    return None

    def __contains__(self, key):
        if self._root is None:
            return None

        parent = None
        node = self._root
        direction = 0

        while True:
            if node is None:
                return False
            if key == node.key:
                return True
            else:
                direction = 0 if key <= node.key else 1
                parent = node
                node = parent[direction]

    def __min__(self):
        return self.min_node()

    def min_node(self):
        if self._root is None:
            raise ValueError('BSTree is empty.')

        min_node = self._root

        while True:
            if min_node[0] is None:
                return min_node
            else:
                min_node = min_node[0]

    def __max__(self):
        return self.max_node()

    def max_node(self):
        if self._root is None:
            raise ValueError('BSTree is empty.')

        max_node = self._root

        while True:
            if max_node[1] is None:
                return max_node
            else:
                max_node = max_node[1]
