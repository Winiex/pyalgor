from .tree import TNode, Tree, DFIter, BFIter


def subtree_min(root, tree):
    """
    Find the node with minimium key in a BSTree subtree.

    root - the subtree's root node.

    tree - the tree instance.
    """
    if tree._node_empty(root):
        raise ValueError('Root node should not be None.')

    if tree._node_empty(root.left):
        return root

    node = root

    while True:
        if not tree._node_empty(node[0]):
            node = node[0]
            continue
        else:
            break

    return node


def subtree_max(root, tree):
    """
    Find the node with maximium key in a BSTree subtree.

    root - the subtree's root node.

    tree - the tree instance.
    """
    if tree._node_empty(root):
        raise ValueError('root node should not be None.')

    if tree._node_empty(root.right):
        return root

    node = root

    while True:
        if not tree._node_empty(node[1]):
            node = node[1]
            continue
        else:
            break

    return node


class PreOrderIter(DFIter):
    """
    Pre-order iterator.
    """
    def __init__(self, root, tree):
        super(PreOrderIter, self).__init__(root, tree)

    def _get_next(self):
        frame = self._pop_stack()

        if frame is None:
            return None

        node = frame[0]

        self._push_stack(node[1], 0)
        self._push_stack(node[0], 0)
        return node


class InOrderIter(DFIter):
    """
    In-order iterator.
    """
    def __init__(self, root, tree):
        super(InOrderIter, self).__init__(root, tree)

    def _get_next(self):
        frame = self._pop_stack()

        if frame is None:
            return None

        node = frame[0]
        child_to = frame[1]

        if child_to == 1:
            self._push_stack(node[1], 0)
            return node

        while True:
            if not self._node_empty(node[0]):
                self._push_stack(node, 1)
                node = node[0]
            else:
                self._push_stack(node[1], 0)
                return node


class PostOrderIter(DFIter):
    """
    Post-order iterator.
    """
    # The CONTINUE object is used to
    # decide whether we should invoke
    # the "_get_next" method again in the
    # "next" method until we get the node
    # returned next.
    CONTINUE = object()

    def __init__(self, root, tree):
        super(PostOrderIter, self).__init__(root, tree)
        self.__previous = None
        self.__current = None

    def _get_next(self):
        frame = self._stack_top()

        if frame is None:
            return None

        result = self.CONTINUE

        # The child_to is not used in procedure followed,
        # so we don't access it, and just store 0 in the
        # frame.
        self.__current = frame[0]

        if self._node_empty(self.__previous) or \
           self.__previous.left is self.__current or \
           self.__previous.right is self.__current:

            if not self._node_empty(self.__current.left):
                self._push_stack(self.__current.left, 0)
            elif not self._node_empty(self.__current.right):
                self._push_stack(self.__current.right, 0)
            else:
                self._pop_stack()
                result = self.__current

        elif self.__current.left is self.__previous:

            if not self._node_empty(self.__current.right):
                self._push_stack(self.__current.right, 0)
            else:
                self._pop_stack()
                result = self.__current

        elif self.__current.right is self.__previous:
            self._pop_stack()
            result = self.__current

        self.__previous = self.__current

        return result

    def next(self):
        while True:
            result = self._get_next()

            if result is self.CONTINUE:
                # When it returns CONTINUE object,
                # we should invoke _get_next method
                # again.
                continue
            elif result is None:
                raise StopIteration()
            else:
                return result


class BSTNode(TNode):
    """
    Binary search tree node.
    """

    __slots__ = ('_key', '_value', '_children',
                 '_height', '_parent', '__left', '__right')

    def __init__(self, key, value, height,
                 parent, left=None, right=None):
        children = [left, right]

        super(BSTNode, self).__init__(
            key, value, height, parent, children
        )

        self.__left = left
        self.__right = right

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, left):
        self.__left = left
        self._children[0] = left

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, right):
        self.__right = right
        self._children[1] = right

    @property
    def parent_side(self):
        """
        Judges the node is on which side of its parent.

        On the left returns 0, on the right returns 1.
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


class BSTree(Tree):
    """
    Binary search tree.
    """

    _allowed_iters = (DFIter, BFIter, PreOrderIter,
                      InOrderIter, PostOrderIter)

    def __init__(self, root=None, iter_type=None):
        super(BSTree, self).__init__(root, iter_type)

    def __new_node(self, key, value, height, parent,
                   left=None, right=None):
        return BSTNode(key, value, height, parent,
                       left, right)

    def insert(self, key, value):
        if self._node_empty(self._root):
            self._root = self.__new_node(key, value, 1, None)
            self._height = 1
        else:
            parent = None
            direction = 0  # 0 means left, 1 means right.
            node = self._root

            while True:
                if self._node_empty(node):
                    parent[direction] = self.__new_node(
                        key, value, parent.height + 1, parent
                    )

                    # When you insert a node right after your
                    # removing a node, the height of the tree
                    # needs rebuilding.
                    if self._height_rebuild_needed:
                        self._rebuild_tree_height()

                    if self.height < parent.height + 1:
                        # We should update the tree's height
                        # when the node newly inserted has the
                        # maximium height in the tree.
                        self._height = parent.height + 1

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

    def _remove(self, node):
        """
        Removes the specific node from the tree.o
        """
        if self._is_root(node):
            successor = self._successor(node)

            if not self._node_empty(successor):
                # node has successor.
                node.key = successor.key
                node.value = successor.value

                if successor.parent_side == 0:
                    successor.parent.left = successor.right
                else:
                    successor.parent.right = successor.right

                if not self._node_empty(successor.right):
                    successor.right.parent = successor.parent
                    successor.right.height = successor.height

                self._refresh_nodes_height(successor.right)
                successor.free()
            else:
                predecessor = self._predecessor(node)

                if self._node_empty(predecessor):
                    # This means there's only root node
                    # in the tree. The node has no successor
                    # or predecessor.
                    self._root.free()
                    self._root = None
                else:
                    # node has predecessor.
                    node.key = predecessor.key
                    node.value = predecessor.value

                    if predecessor.parent_side == 0:
                        predecessor.parent.left = predecessor.left
                    else:
                        predecessor.parent.right = predecessor.left

                    if not self._node_empty(predecessor.left):
                        predecessor.left.parent = predecessor.parent
                        predecessor.left.height = predecessor.height

                    self._refresh_nodes_height(predecessor.left)
                    predecessor.free()
        else:
            if node.is_leaf():
                if node.parent_side == 0:
                    node.parent.left = None
                else:
                    node.parent.right = None

                node.free()
            else:
                if not self._node_empty(node.left) and \
                   not self._node_empty(node.right):
                    successor = self._successor(node)

                    node.key = successor.key
                    node.value = successor.value

                    if successor.parent_side == 0:
                        successor.parent.left = successor.right
                    else:
                        successor.parent.right = successor.right

                    if not self._node_empty(successor.right):
                        successor.right.parent = successor.parent
                        successor.right.height = successor.height

                    self._refresh_nodes_height(successor.right)
                    successor.free()
                else:
                    if not self._node_empty(node.left):
                        if node.parent_side == 0:
                            node.parent.left = node.left
                        else:
                            node.parent.right = node.left

                        node.left.parent = node.parent
                        node.left.height = node.height

                        self._refresh_nodes_height(node.left)
                        node.free()
                    else:
                        if node.parent_side == 0:
                            node.parent.left = node.right
                        else:
                            node.parent.right = node.right

                        node.right.parent = node.parent
                        node.right.height = node.height

                        self._refresh_nodes_height(node.right)
                        node.free()

        self._height_rebuild_needed = True

    def remove(self, key):
        """
        Removes the node with specific key
        from the tree.
        """
        node = self.search(key)

        self._remove(node)

    def search(self, key):
        """
        Searches for a node with the specified key.

        Raise KeyError if the node doesn't exist.
        """
        if self._node_empty(self._root):
            raise ValueError('Tree is empty.')

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

                if self._node_empty(node):
                    raise KeyError('key %s doesn\'t exist.' % key)

    def _successor(self, node):
        """
        Gets the successor of a node.

        Returns None if the successor doesn't exist.
        """
        if not self._node_empty(node.right):
            return subtree_min(node.right, self)

        parent = node.parent

        while (not self._node_empty(parent) and
               node is parent.right):
            node = parent
            parent = node.parent

        return parent

    def successor(self, key):
        """
        Gets the successor of a node with the specified key.

        Returns None if the successor doesn't exist.
        """
        node = self.search(key)

        return self._successor(node)

    def _predecessor(self, node):
        """
        Gets the predecessor of a node.

        Returns None if the predecessor doesn't exist.
        """
        if not self._node_empty(node.left):
            return subtree_max(node.left, self)

        parent = node.parent

        while (not self._node_empty(parent) and
               node is parent.left):
            node = parent
            parent = node.parent

        return parent

    def predecessor(self, key):
        """
        Gets the predecessor of a node with the specified key.

        Returns None if the predecessor doesn't exist.
        """
        node = self.search(key)

        return self._predecessor(node)

    def __contains__(self, key):
        if self._node_empty(self._root):
            return None

        parent = None
        node = self._root
        direction = 0

        while True:
            if self._node_empty(node):
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
        if self._node_empty(self._root):
            raise ValueError('BSTree is empty.')

        return subtree_min(self._root, self)

    def __max__(self):
        return self.max_node()

    def max_node(self):
        if self._node_empty(self._root):
            raise ValueError('BSTree is empty.')

        return subtree_max(self._root, self)

    def _left_rotate(self, node):
        """
             |                     |
            (y)                   (x) <-- this is a tree node.
            / \     left rotate   / \
          (x)  c   <------------ a  (y)
          / \                       / \
         a   b                     b   c <-- this is a subtree.

        The paramater "node" is the x node in the right tree.
        """
        if self._node_empty(node.right):
            raise ValueError('node\'s right child shouldn\'t be None.')

        right_child = node.right
        parent = node.parent

        right_child.parent = node.parent
        right_child.height = node.height

        if not self._is_root(node):
            if node is parent.left:
                parent.left = right_child
            elif node is parent.right:
                parent.right = right_child
        else:
            self._root = right_child

        node.right = right_child.left

        if not self._node_empty(right_child.left):
            right_child.left.parent = node

        right_child.left = node

        node.parent = right_child

        self._refresh_nodes_height(right_child)
        self._height_rebuild_needed = True

    def left_rotate(self, key):
        node = self.search(key)

        self._left_rotate(node)

    def _right_rotate(self, node):
        """
             |                       |
            (y)                     (x) <-- This is a tree node.
            / \     Right rotate    / \
          (x)  c   ------------->  a  (y)
          / \                         / \
         a   b                       b   c <-- This is a subtree.

        The paramater "node" is the y node in the left tree.
        """
        if self._node_empty(node.right):
            raise ValueError('node\'s left child shouldn\'t be None.')

        left_child = node.left
        parent = node.parent

        left_child.parent = node.parent
        left_child.height = node.height

        if not self._is_root(node):
            if parent.left is node:
                parent.left = left_child
            elif parent.right is node:
                parent.right = left_child
        else:
            self._root = left_child

        node.left = left_child.right

        if not self._node_empty(left_child.right):
            left_child.right.parent = node

        left_child.right = node

        node.parent = left_child

        self._refresh_nodes_height(left_child)
        self._height_rebuild_needed = True

    def right_rotate(self, key):
        node = self.search(key)

        self._right_rotate(node)

    def transplant(self, from_key, to_key):
        """
        Transplants node with from_key and its subtree
        to positio of node with to_key.
        """
        from_node = self.search(from_key)
        to_node = self.search(to_key)

        self._transplant(from_node, to_node)
