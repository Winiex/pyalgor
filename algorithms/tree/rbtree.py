from .bstree import BSTree, BSTNode


class Color(object):
    """
    Color object represents the RBTNode's color.
    """

    BLACK = 0
    RED = 1

    __allowed_colors = (BLACK, RED)

    def __init__(self, color):
        if color not in self.__allowed_colors:
            raise ValueError('color value invalid,'
                             'it should be 0(BLACK) or 1(RED)')
        self.__color = color

    def __repr__(self):
        if self.__color == 0:
            return '<Color: value 0, color BLACK>'
        else:
            return '<Color: value 1, color RED>'

    def __str__(self):
        return 'BLACK' if self.__color == 0 else 'RED'

    @classmethod
    def black(self):
        return Color(Color.BLACK)

    @classmethod
    def red(self):
        return Color(Color.RED)

    # It's not elegant to do color changing likes
    # "rbt.root.color.color = Color.BLACK". With turn_black
    # and turn_red methods, color changing could be like
    # "rbt.root.color.turn_black()".
    def turn_black(self):
        self.__color = Color.BLACK

    def turn_red(self):
        self.__color = Color.RED

    def is_black(self):
        if self.__color == 0:
            return True
        else:
            return False

    def is_red(self):
        if self.__color == 1:
            return True
        else:
            return False


class RBTNode(BSTNode):

    __slots__ = ('_key', '_value', '_children',
                 '_height', '_parent', '__color',
                 '__left', '__right')

    def __init__(self, key, value, height,
                 parent, color, left=None, right=None):
        super(RBTNode, self).__init__(
            key, value, height, parent, left, right
        )

        self.__color = color

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color

    def free(self):
        super(RBTNode, self).free()
        self.color = None

    def __repr__(self):
        if self is RBTree.NIL:
            return '<RBTNode: NIL>'

        repr_info = [self.key, self.value]

        if self.color.is_black():
            repr_info.append('BLACK')
        elif self.color.is_red():
            repr_info.append(('RED'))

        return '<RBTNode: key %s, value %s, color %s>' \
            % tuple(repr_info)


class RBTree(BSTree):

    NIL = RBTNode(None, None, -1, None,
                  Color.black(), None, None)

    def __init__(self, root=None, iter_type=None):
        super(RBTree, self).__init__(root, iter_type)
        if root is None:
            self._root = self.NIL

    def __new_node(self, key, value, height, parent,
                   color, left=None, right=None):
        return RBTNode(key, value, height, parent,
                       color, self.NIL, self.NIL)

    def _is_root(self, node):
        """
        Judges whether the node is the root.o

        Because when a RBTNode is the root, it's parent
        isn't None but RBTree.NIL, causing the result of
        Tree._is_root being not correct. Because of
        this, we should define the RBTree's own _is_root.
        """
        return node.parent is self.NIL

    def insert(self, key, value):
        new_node = self.NIL

        if self._root is self.NIL:
            self._root = self.__new_node(key, value, 1,
                                         self.NIL, Color.black())
            self._height = 1
            new_node = self._root
        else:
            parent = self.NIL
            direction = 0
            node = self._root

            while True:
                if node is self.NIL:
                    parent[direction] = self.__new_node(
                        key, value, parent.height + 1, parent,
                        Color.red()
                    )

                    new_node = parent[direction]

                    # When you insert a node right after your
                    # removing a node, the height of the tree
                    # needs rebuilding.
                    if self._height_rebuild_needed:
                        self._rebuild_height()

                    if self.height < parent.height + 1:
                        # We should update the tree's height
                        # when the node newly inserted has the
                        # maximium height in the tree.
                        self._height = parent.height + 1

                    break
                if key == node.key:
                    node.value = value
                    new_node = node
                    break
                else:
                    parent = node
                    direction = 0 if key <= node.key else 1
                    node = node[direction]

        self._count += 1
        self.__fix_insert(new_node)

        return self

    def __fix_insert(self, new_node):
        node_to_fix = new_node

        while True:
            if self._is_root(node_to_fix):
                node_to_fix.color.turn_black()
                break

            parent = node_to_fix.parent

            if self._is_root(parent):
                # Root node is made black after every node insertion.
                # This ensures parent has parent :).
                break

            if parent.color.is_black():
                break

            if parent is parent.parent.left:
                uncle = parent.parent.right
            elif parent is parent.parent.right:
                uncle = parent.parent.left

            if node_to_fix is parent.left:

                if uncle is self.NIL:
                    # The new_node has no uncle. The transformation
                    # is shown below(x is the new_node):
                    #          |
                    #    (parent(BLACK))  <--- Left rotation happens here.
                    #      /                                  |
                    #    (y(RED))                          (y(RED))
                    #    /           transform              /   \
                    #  (x(RED))     ----------->    (x(BLACK)) (parent(BLACK))
                    #  /                                 /
                    # a                                 a
                    node_to_fix.color.turn_black()
                    self._right_rotate(parent.parent)
                    break

                if uncle.color.is_black():

                    parent.color.turn_black()
                    parent.parent.color.turn_red()
                    self._right_rotate(parent.parent)
                    break

                elif uncle.color.is_red():

                    parent.color.turn_black()
                    uncle.color.turn_black()
                    parent.parent.color.turn_red()
                    node_to_fix = parent.parent

            elif node_to_fix is parent.right:

                if uncle is self.NIL:
                    node_to_fix.color.turn_black()
                    self._left_rotate(parent.parent)
                    break

                if uncle.color.is_black():

                    parent.color.turn_black()
                    parent.parent.color.turn_red()
                    self._left_rotate(parent.parent)
                    break

                elif uncle.color.is_red():

                    parent.color.turn_black()
                    uncle.color.turn_black()
                    parent.parent.color.turn_red()
                    node_to_fix = parent.parent

    def remove(self, key, value):
        pass
