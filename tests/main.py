import unittest


from algorithms.tree import BSTree, DFIter, \
    PreOrderIter, InOrderIter, PostOrderIter


class TestBSTree(unittest.TestCase):

    def setUp(self):
        pass

    def test_insert(self):
        bst = BSTree()
        bst.insert(1, 2).insert(0, 1).insert(2, 3)

    def test_dft(self):
        bst = BSTree(iter_type=DFIter)
        bst.insert(1, 2).insert(0, 1).insert(2, 3).insert(-1, 1)

    def test_contains(self):
        bst = BSTree()
        bst.insert(1, 2).insert(2, 3).insert(3, 4)

        self.assertTrue(1 in bst)
        self.assertFalse(9 in bst)

    def test_remove(self):
        bst = BSTree()
        bst.insert(1, 2).insert(0, 1).insert(2, 3)

        self.assertTrue(1 in bst)

        bst.remove(1)

        self.assertFalse(1 in bst)

    def test_pre_order_iter(self):
        print 'test_pre_order_iter'
        bst = BSTree(iter_type=PreOrderIter)
        bst.insert(1, 2).insert(0, 1).insert(2, 3).insert(-1, 1) \
            .insert(0.5, 1)

        for node in bst:
            print node

    def test_in_order_iter(self):
        print 'test_in_order_iter'
        bst = BSTree(iter_type=InOrderIter)
        bst.insert(1, 2).insert(0, 1)

        for node in bst:
            print node

    def test_post_order_iter(self):
        print 'test_post_order_iter'
        bst = BSTree(iter_type=PostOrderIter)
        bst.insert(1, 2).insert(0, 1).insert(2, 3).insert(-1, 1) \
            .insert(0.5, 1)

        for node in bst:
            print node


if __name__ == '__main__':
    unittest.main()
