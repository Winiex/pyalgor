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
