class DFIter(object):
    """Deep first traverse iterator.
    In post-order."""

    def __init__(self, tree):
        self.__tree = tree
        self._trave_stack = []

        if tree.root is not None:
            self._trave_stack.append((tree.root, 0))

    def _get_child_to(self, node, start):
        """Find the next child_to index.
        The child_to index is the index of the
        node's child to be visited next."""

        child_to = start
        for i in xrange(start, node.children_len):
            if node[i] is None:
                child_to += 1
            else:
                break

        return child_to

    def _push_stack(self, node, child_to):
        if node is None:
            return

        self._trave_stack.append((node, child_to))

    def _pop_stack(self):
        try:
            frame = self._trave_stack.pop()
        except IndexError:
            return None

        return frame

    def _get_next(self):
        frame = self._pop_stack()

        if frame is None:
            return None

        node = frame[0]
        start = frame[1]

        while True:
            child_to = self._get_child_to(node, start)

            if child_to == node.children_len:
                return node
            else:
                self._push_stack(node, child_to + 1)

                node = node[child_to]
                start = 0

    def __iter__(self):
        return self

    def next(self):
        node = self._get_next()

        if node is None:
            raise StopIteration()

        return node

    __next__ = next


class BFIter(object):
    """Breadth first traverse iterator"""
    def __init__(self, tree):
        self.__tree = tree
        self._trave_list = []
        if tree.root is not None:
            self._trave_list.append(self.__tree.root)

    def __iter__(self):
        return self

    def next(self):
        try:
            node = self._trave_list.pop(0)
        except IndexError:
            raise StopIteration()

        for child in node.children:
            if child is not None:
                self._trave_list.append(child)

        return node

    __next__ = next


class BaseNode(object):
    """Basic node."""
    __slots__ = ('_key', '_value', '_children')

    def __init__(self, key, value, children=[]):
        self._key = key
        self._value = value
        self._children = children

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def children(self):
        return self._children

    @property
    def children_len(self):
        return len(self._children)

    @property
    def child_count(self):
        """Return the number of child non-None."""
        count = 0
        for child in self._children:
            if child is not None:
                count += 1

        return count

    def __getitem__(self, key):
        """Access children of node using indexing format."""
        if not isinstance(key, int):
            raise TypeError('Key should be an int type.')

        children_length = len(self._children)

        if key < -children_length or key >= children_length:
            raise IndexError('Key out of range.')

        return self._children[key]

    def __setitem__(self, key, value):
        """Assign the child of node using indexing format."""
        if not isinstance(key, int):
            raise TypeError('Key should be an int type.')

        children_length = len(self._children)

        if key < -children_length or key >= children_length:
            raise IndexError('Key out of range.')

        self._children[key] = value

    def free(self):
        self._key = None
        self._value = None
        self._children = None


class BaseTree(object):
    """The basic tree structure.
    Common operations on trees are defined here."""
    _allowed_iters = (DFIter, BFIter)

    def __init__(self, root=None, iter_type=None):
        self._root = root
        self._count = 0
        self._iter_type = iter_type

    def __contains__(self, key):
        for node in self:
            if key == node.key:
                return True

    def __iter__(self):
        if self._iter_type is None:
            self._iter_type = DFIter

        iter_type = self._iter_type
        if iter_type not in self._allowed_iters:
            raise TypeError('iter_type %r error.' % self._iter_type)

        return iter_type(self)

    @property
    def root(self):
        return self._root

    @property
    def count(self):
        return self._count

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __xor__(self, other):
        pass

    def min_node(self):
        if self._root is None:
            raise ValueError('Tree is empty.')

        min_node = self._root

        for node in self:
            if min_node.key > node.key:
                min_node = node

        return min_node

    def __min__(self):
        return self.min_node()

    def max_node(self):
        if self._root is None:
            raise ValueError('Tree is empty.')

        max_node = self._root

        for node in self:
            if max_node.key < node.key:
                max_node = node

        return max_node

    def __max__(self):
        return self.max_node()
