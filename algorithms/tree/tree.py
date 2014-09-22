class Iter(object):

    def __init__(self, root, tree):
        self._root = root
        self._tree = tree

    def __iter__(self):
        return self

    def next(self):
        raise NotImplementedError(
            'You need to implement the next method.'
        )

    def _node_empty(self, node):
        return self._tree._node_empty(node)

    __next__ = next


class DFIter(Iter):
    """
    Deep first traverse iterator. Default in post-order.

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
    in accessing the node's children using index
    manner.

    "node[0]" means getting node's first child node.
    """
    def __init__(self, root, tree):
        super(DFIter, self).__init__(root, tree)
        self._iter_stack = []

        if not self._node_empty(root):
            self._iter_stack.append((root, 0))

    def _get_child_to(self, node, start):
        """
        Find the next child_to index.
        The child_to index is the index of the
        node's child to be visited next.
        """
        child_to = start
        for i in xrange(start, node.children_len):
            if self._node_empty(node[i]):
                child_to += 1
            else:
                break

        return child_to

    def _push_stack(self, node, child_to):
        if self._node_empty(node):
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

    def next(self):
        result = self._get_next()

        if result is None:
            raise StopIteration()

        return result


class BFIter(Iter):
    """
    Breadth first traverse iterator.
    """
    def __init__(self, root, tree):
        super(BFIter, self).__init__(root, tree)
        self._trave_list = []

        if not self._node_empty(root):
            self._trave_list.append(root)

    def next(self):
        try:
            node = self._trave_list.pop(0)
        except IndexError:
            raise StopIteration()

        for child in node.children:
            if not self._node_empty(child):
                self._trave_list.append(child)

        return node


class TNode(object):
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
                 parent, children=None):
        self._key = key
        self._value = value
        self._parent = parent
        self._height = height

        if children is None:
            self._children = []
        else:
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
            if not self._node_empty(child):
                count += 1

        return count

    def is_leaf(self):
        """
        Judges whether a node is a leaf node.
        """
        if not self.children:
            # self.children is []
            return True

        for child in self.children:
            if self._node_empty(child):
                return False

        return True

    def __getitem__(self, key):
        """
        Access children of node using indexing format.
        """
        if not self.children:
            raise ValueError('TNode %s has no children.'
                             % self.key)

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

    def __repr__(self):
        return '<TNode: key %s, value %s>' % \
            (self.key, self.value)

    def __str__(self):
        return str(self.key)

    def free(self):
        self._key = None
        self._value = None
        self._children = None
        self._height = 0
        self._parent = None


class Tree(object):
    """
    The basic tree structure.
    Common operations on trees are defined here.

    root - The root node of the tree.

    count - The number of nodes in the tree.

    iter_type - The iteration type you want to do
    on your tree. For example,

    tree = Tree(iter_type=DFIter)

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

        return False

    def __iter__(self):
        if self._iter_type is None:
            iter_type = DFIter
        else:
            iter_type = self._iter_type

        self._check_iter(iter_type)

        return iter_type(self._root, self)

    def _check_iter(self, iter_type):
        if iter_type not in self._allowed_iters:
            raise TypeError('iter_type %r error.' % self._iter_type)

    def _is_root(self, node):
        return node.parent is None

    @property
    def root(self):
        return self._root

    @property
    def count(self):
        return self._count

    @property
    def height(self):
        if self._height_rebuild_needed:
            self._height = self._rebuild_tree_height()

        return self._height

    def _refresh_nodes_height(self, root_node):
        """
        Refresh the height of all the nodes in a subtree.
        """
        def refresh_child_height(node):
            for child in node.children:
                if not self._node_empty(child):
                    child.height = node.height + 1

        self.iterate(root_node, refresh_child_height, BFIter)

    def _rebuild_tree_height(self):
        """
        Rebuild the height of the tree.
        """
        if self._node_empty(self._root):
            return 0

        height = self.root.height

        for node in self:
            if height < node.height:
                height = node.height

        return height

    def _node_empty(self, node):
        return node is None

    @property
    def iter_type(self):
        return self._iter_type

    @iter_type.setter
    def iter_type(self, iter_type):
        self._iter_type = iter_type

    def is_empty(self):
        return self._node_empty(self._root)

    def __new_node(self, key, value, height, parent):
        return TNode(
            key, value, height, parent
        )

    def insert(self, key, value,
               parent_key=None, which_parent=None):
        if self.is_empty():
            self._root = self.__new_node(
                key, value, 1, None
            )

            self._height = 1
        else:
            if parent_key is None or \
               which_parent is None:
                raise ValueError('parent_key or which_parent '
                                 'shouldn\'t be None '
                                 'when root node exists.')

            try:
                parent = self.search(parent_key, which_parent)
            except KeyError:
                raise KeyError('parent node with key %s '
                               'not found.' % parent_key)

            new_node = self.__new_node(
                key, value, parent.height + 1, parent
            )

            parent.children.append(new_node)

            if new_node.height > self.height:
                self._height = new_node.height

        self._count += 1
        return self

    def remove(self, key, which):
        node = self.search(key, which)

        parent = node.parent

        for index, child in enumerate(parent.children):
            if child is node:
                parent[index] = None

    def search(self, key, which=1):
        """
        Searches for a node with key in the tree.
        The searching process uses breadth first
        iteration.

        which - There may exist nodes with same in the
        same tree. You can use "which" to specify which
        you need. For example:

        self.search(1, 2)

        means you need the second node with key 1 in the
        breadth first iteration process. "which" starts
        from 1, not 0.
        """

        if which <= 0:
            raise ValueError('which should be positive.')

        count = 1
        result = None

        origin_iter_type = self.iter_type

        self.iter_type = BFIter

        for node in self:
            if node.key == key:
                if count == which:
                    result = node
                    break
                else:
                    count += 1

        self.iter_type = origin_iter_type

        if result is None:
            # Finally we don't find it.
            raise KeyError('node with key %s '
                           'not found.' % key)

        return result

    def _transplant(self, from_node, to_node):
        """
        Transplants from_node and its subtree
        to to_node's position.
        """
        if self._is_root(to_node):
            self._root = from_node
            self._root.height = 1
            self._refresh_nodes_height(self._root)
            self._height_rebuild_needed = True
        else:
            to_parent = to_node.parent
            from_parent = from_node.parent

            for index, child in enumerate(from_parent.children):
                if child is from_node:
                    from_parent[index] = None

            for index, child in enumerate(to_parent.children):
                if child is to_node:
                    to_parent[index] = from_node

            from_node.parent = to_parent
            from_node.height = to_parent.height + 1

            self._refresh_nodes_height(from_node)
            self._height_rebuild_needed = True

        # Free the to_node and it's child nodes.
        def free(node):
            node.free()

        self.iterate(to_node, free, BFIter)

    def transplant(self, from_key, to_key,
                   which_from=1, which_to=1):
        """
        Transplants node with from_key and its subtree
        to positio of node with to_key.
        """
        from_node = self.search(from_key, which_from)
        to_node = self.search(to_key, which_to)

        self._transplant(from_node, to_node)

    def iterate(self, root_node, operation, iter_type=None):
        """
        Iterates over subtree with root node "root_node".
        On every node, operation is taken. Operation is
        a function like this:

        def print_node(node):
            print node.key, node.value

        Then you can use operation on a tree:

        tree.iterate(tree.root, print_node)

        The iteration type is defined by iter_type paramater.
        If iter_type paramater is None, the tree's iter_type
        is used.
        """
        if iter_type is None:
            if self._iter_type is None:
                iter_type = BFIter
            else:
                iter_type = self.iter_type
        else:
            self._check_iter(iter_type)

        nodes = iter_type(root_node, self)

        for node in nodes:
            operation(node)

    def min_node(self):
        if self._node_empty(self._root):
            raise ValueError('Tree is empty.')

        min_node = self._root

        for node in self:
            if min_node.key > node.key:
                min_node = node

        return min_node

    def max_node(self):
        if self._node_empty(self._root):
            raise ValueError('Tree is empty.')

        max_node = self._root

        for node in self:
            if max_node.key < node.key:
                max_node = node

        return max_node

    def __and__(self, other):
        #TODO
        pass

    def __or__(self, other):
        #TODO
        pass

    def __add__(self, other):
        #TODO
        pass

    def __sub__(self, other):
        #TODO
        pass

    def __xor__(self, other):
        #TODO
        pass

    def __max__(self):
        return self.max_node()

    def __min__(self):
        return self.min_node()
