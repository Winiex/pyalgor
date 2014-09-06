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


class BaseTree(object):
    """The basic tree structure.
    Common operations on trees are defined here."""
    def __init__(self):
        self.__root = None

    def __contains__(self, key):
        pass

    def __iter__(self):
        pass
