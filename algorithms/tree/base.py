class DFIter(object):
    """Deep first traverse iterator"""
    def __init__(self, tree):
        self.__tree = tree
        self.__trave_stack = []
        if tree.root is not None:
            self.__trave_stack.append((tree.root, 0))

    def __get_child_to(self, node, start):
        child_to = start
        # Find the next child_to index.
        for i in xrange(start, node.children_len):
            if node[i] is None:
                child_to += 1
            else:
                break

        return child_to

    def _get_next(self):
        try:
            frame = self.__trave_stack.pop()
        except IndexError:
            return None

        node = frame[0]
        start = frame[1]

        while True:
            child_to = self.__get_child_to(node, start)

            if child_to == node.children_len:
                return node
            else:
                self.__trave_stack.append(
                    (node, child_to + 1)
                )

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
        self.__trave_list = []
        if tree.root is not None:
            self.__trave_list.append(self.__tree.root)

    def __iter__(self):
        return self

    def next(self):
        try:
            node = self.__trave_list.pop(0)
        except IndexError:
            raise StopIteration()

        for child in node.children:
            if child is not None:
                self.__trave_list.append(child)

        return node

    __next__ = next


class BaseNode(object):
    """Basic node."""
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

    @children.setter
    def children(self, children):
        self._children = children

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
    __allowed_iters = (DFIter, BFIter)

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
            self._iter_type = BFIter

        iter_type = self._iter_type
        if iter_type not in self.__allowed_iters:
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
