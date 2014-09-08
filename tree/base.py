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
        self.__key = key
        self.__value = value
        self.__children = children

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key):
        self.__key = key

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, children):
        self.__children = children

    @property
    def children_len(self):
        return len(self.__children)

    @property
    def child_count(self):
        """Return the number of child non-None."""
        count = 0
        for child in self.__children:
            if child is not None:
                count += 1

        return count

    def __getitem__(self, key):
        """Access children of node using indexing format."""
        if not isinstance(key, int):
            raise TypeError('Key should be an int type.')

        children_length = len(self.__children)

        if key < -children_length or key >= children_length:
            raise IndexError('Key out of range.')

        return self.__children[key]

    def __setitem__(self, key, value):
        """Assign the child of node using indexing format."""
        if not isinstance(key, int):
            raise TypeError('Key should be an int type.')

        children_length = len(self.__children)

        if key < -children_length or key >= children_length:
            raise IndexError('Key out of range.')

        self.__children[key] = value

    def free(self):
        self.__key = None
        self.__value = None
        self.__children = None


class BaseTree(object):
    """The basic tree structure.
    Common operations on trees are defined here."""
    __allowed_iters = (DFIter, BFIter)

    def __init__(self, root=None, iter_type=None):
        self.__root = root
        self.__count = 0
        self.__iter_type = iter_type

    def __contains__(self, key):
        pass

    def __iter__(self):
        iter_type = self.__iter_type
        if iter_type not in self.__allowed_iters:
            raise TypeError('iter_type %r error.' % self.__iter_type)

        return iter_type(self)

    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, node):
        self.__root = node

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, count):
        self.__count = count
