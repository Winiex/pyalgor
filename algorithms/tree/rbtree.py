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

    # It's not elegant to deal with color changing likes
    # "rbt.root.color.color = Color.BLACK". Using turn_black
    # and turn_red methods, color changing could be like
    # "rbt.root.color.turn_black()", which is more self-explained.
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
    # Using __slots__ property makes node object occupy less memory.
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

    def is_leaf(self):
        if not self.children:
            # self.children is []
            return True

        for child in self.children:
            if child is not RBTree.NIL:
                return False

        return True

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
        Judges whether the node is the root.

        Because when a RBTNode is the root, it's parent
        isn't None but RBTree.NIL, causing the result of
        Tree._is_root being not correct. Because of
        this, we should define the RBTree's own _is_root.
        """
        return node.parent is self.NIL

    def _node_empty(self, node):
        return node is self.NIL

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
                if self._node_empty(node):
                    parent[direction] = self.__new_node(
                        key, value, parent.height + 1,
                        parent, Color.red()
                    )

                    new_node = parent[direction]

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

    def _remove(self, node):
        node_to_fix = None
        removal_color = None

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

                node_to_fix = successor.right
                removal_color = Color.black() \
                    if successor.color.is_black() \
                    else Color.red()

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

                    node_to_fix = predecessor.left
                    removal_color = Color.black() \
                        if predecessor.color.is_black() \
                        else Color.red()
                    predecessor.free()
        else:
            if node.is_leaf():
                if node.parent_side == 0:
                    node.parent.left = None
                else:
                    node.parent.right = None

                node_to_fix = node.right
                removal_color = Color.black() \
                    if node.right.color.is_black() \
                    else Color.red()
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

                    node_to_fix = successor.right
                    removal_color = Color.black() \
                        if successor.color.is_black() \
                        else Color.red()
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

                        node_to_fix = node.left
                        node.free()
                    else:
                        if node.parent_side == 0:
                            node.parent.left = node.right
                        else:
                            node.parent.right = node.right

                        node.right.parent = node.parent
                        node.right.height = node.height

                        self._refresh_nodes_height(node.right)

                        node_to_fix = node.right
                        node.free()

                    removal_color = Color.black() \
                        if node.color.is_black() \
                        else Color.red()

        self._height_rebuild_needed = True

        if node_to_fix is not None and \
           removal_color is not None and \
           removal_color.is_black():
            self.__fix_remove(node_to_fix)

    def __fix_remove(self, node):
        node_to_fix = node
        while (node_to_fix.color.is_black() and
               not self._is_root(node_to_fix)):

            if node_to_fix.parent_side == 0:
                uncle = node_to_fix.parent.right

                if uncle.color.is_red():
                    uncle.color.turn_black()
                    node_to_fix.parent.color.turn_red()
                    self.left_rotate(node_to_fix.parent)
                    uncle = node_to_fix.parent.right

                if uncle.left.color.is_black() and \
                   uncle.right.color.is_black():
                    uncle.color.turn_red()
                    node_to_fix = node_to_fix.parent
                elif uncle.right.color.is_black():
                    uncle.left.color.turn_black()
                    uncle.color.turn_red()
                    self.right_rotate(uncle)
                    uncle = node_to_fix.parent.right
                else:
                    uncle.color = Color.black() \
                        if node_to_fix.parent.color.is_black() \
                        else Color.red()

                    node_to_fix.parent.color.turn_black()
                    uncle.right.color.turn_black()
                    self.left_rotate(node_to_fix.parent)
                    node_to_fix = self._root
            else:
                uncle = node_to_fix.parent.left

                if uncle.color.is_red():
                    uncle.color.turn_black()
                    node_to_fix.parent.color.turn_red()
                    self.right_rotate(node_to_fix.parent)
                    uncle = node_to_fix.parent.left

                if uncle.right.color.is_black() and \
                   uncle.left.color.is_black():
                    uncle.color.turn_red()
                    node_to_fix = node_to_fix.parent
                elif uncle.left.color.is_black():
                    uncle.right.color.turn_black()
                    uncle.color.turn_red()
                    self.left_rotate(uncle)
                    uncle = node_to_fix.parent.left
                else:
                    uncle.color = Color.black() \
                        if node_to_fix.parent.color.is_black() \
                        else Color.red()

                    node_to_fix.parent.color.turn_black()
                    uncle.left.color.turn_black()
                    self.right_rotate(node_to_fix.parent)
                    node_to_fix = self._root

        node_to_fix.color.turn_black()

    def remove(self, key):
        node = self.search(key)

        self._remove(node)
