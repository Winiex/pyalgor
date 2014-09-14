class DFIter(object):
    """
    Deep first traverse iterator. In post-order.

    The instance variable _iter_stack is used to help
    the iteration process, it's a stack. Each of its
    stack frame, a tuple is stored. Inside the tuple
    is two members: a node, and the node's next child
    to iterate. For example, a frame would be like
    (<BTNode: key 0, value 1>, 1), which means that
    the next node to iterate is the SECOND child of
    certain BTNode. The second member of the tuple
    is an index starts from 0, just like array does.
    This is because we implement __getitem__ and
    __setitem__ methods in tree node class, results
    in accessing the node's children using index manner.
    "node[0]" means getting node's first child node.
    """

    def __init__(self, tree):
        self.__tree = tree
        self._iter_stack = []

        if tree.root is not None:
            self._iter_stack.append((tree.root, 0))

    def _get_child_to(self, node, start):
        """
        Find the next child_to index.
        The child_to index is the index of the
        node's child to be visited next.
        """

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

        self._iter_stack.append((node, child_to))

    def _pop_stack(self):
        try:
            frame = self._iter_stack.pop()
        except IndexError:
            return None

        return frame

    def _stack_top(self):
        if self._iter_stack:
            return self._iter_stack[-1]
        else:
            return None

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
    """
    Breadth first traverse iterator.
    """
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
    """
    Basic node.

    key - It's an instance of a COMPARABLE type.

    value - A name stores the data you want.

    children - The node's child nodes.

    height - The height of the node. Root node's height
    is 1.
    """
    __slots__ = ('_key', '_value', '_height',
                 '_parent', '_children')

    def __init__(self, key, value, height,
                 parent, children=[]):
        self._key = key
        self._value = value
        self._parent = parent
        self._height = height
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
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def children(self):
        return self._children

    @property
    def children_len(self):
        return len(self._children)

    @property
    def child_count(self):
        """
        Return the number of child non-None.
        """
        count = 0
        for child in self._children:
            if child is not None:
                count += 1

        return count

    def __getitem__(self, key):
        """
        Access children of node using indexing format.
        """
        if not isinstance(key, int):
            raise TypeError('Key should be an int type.')

        children_length = len(self._children)

        if key < -children_length or key >= children_length:
            raise IndexError('Key out of range.')

        return self._children[key]

    def __setitem__(self, key, value):
        """
        Assign the child of node using indexing format.
        """
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
        self._height = 0
        self._parent = None


class BaseTree(object):
    """
    The basic tree structure.
    Common operations on trees are defined here.

    root - The root node of the tree.

    count - The number of nodes in the tree.

    iter_type - The iteration type you want to do
    on your tree. For example,

    tree = BaseTree(iter_type=DFIter)

    means you want to use deep first iteration on
    your tree. Only a few of iteration types is
    allowed to use on your tree, which is decided
    by the class attribute _allowed_iters of the
    tree class.

    height - The tree's height. When there is only
    root node exists in a tree, the tree's height
    is 1.

    height_rebuid - This is a private instance
    variable used to help deciding whether to rebuild
    the height of the tree. This is because when you
    remove a node from your tree, it's hard and not
    efficient to figure out the height of the tree.
    And immediatly rebuild the height right after the
    node removing is not pragmatic. So we should only
    rebuild the height when it's needed. It's kind of
    like lazy evaluation.
    """
    _allowed_iters = (DFIter, BFIter)

    def __init__(self, root=None, iter_type=None):
        self._root = root
        self._count = 0
        self._height = 0
        self._iter_type = iter_type
        self._height_rebuild_needed = False

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

    def _is_root(self, node):
        if node.parent is None:
            return True
        else:
            return False

    @property
    def root(self):
        return self._root

    @property
    def count(self):
        return self._count

    @property
    def height(self):
        if self._height_rebuild_needed:
            self._height = self._rebuild_height()

        return self._height

    @property
    def iter_type(self):
        return self._iter_type

    @iter_type.setter
    def iter_type(self, iter_type):
        self._iter_type = iter_type

    def _rebuild_height(self):
        """
        Rebuild the height of the tree.
        """
        if self.root is None:
            return 0

        height = self.root.height

        for node in self:
            if height < node.height:
                height = node.height

        return height

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

    def _refresh_height(self, root_node):
        """
        Refresh the height of all the nodes of a subtree.
        """
        nodes_list = [root_node]

        while True:
            try:
                node = nodes_list.pop(0)
            except IndexError:
                break

            for child in node.children:
                if child is not None:
                    child.height = node.height + 1
                    nodes_list.append(child)
