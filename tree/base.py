class DFIter(object):
    """Deep first traverse iterator"""
    pass


class BFIter(object):
    """Breadth first traverse iterator"""
    pass


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
    def child_count(self):
        """Return the number of child non-None."""
        count = 0
        for child in self.__children:
            if child is not None:
                count += 1

        return count

    def __getitem(self, key):
        """Access children of node using indexing format."""
        if not isinstance(key, int):
            raise TypeError('Key should be an int type.')

        children_length = len(self.__children)

        if key < -children_length or key >= children_length:
            raise IndexError('Key out of range.')

        return self.__children[key]

    def __setitem(self, key, value):
        """Assign the child of node using indexing format."""
        if not isinstance(key, int):
            raise TypeError('Key should be an int type.')

        children_length = len(self.__children)

        if key < -children_length or key >= children_length:
            raise IndexError('Key out of range.')

        self.__children[key] = value


class BaseTree(object):
    """The basic tree structure.
    Common operations on trees are defined here."""
    def __init__(self, root=None):
        self.__root = root

    def __contains__(self, key):
        pass

    def __iter__(self):
        pass

    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, node):
        self.__root = node
