import unittest


from algorithms.tree import BinarySearchTree, DFIter


class TestBinarySearchTree(unittest.TestCase):

    def setUp(self):
        pass

    def test_insert(self):
        bst = BinarySearchTree()
        bst.insert(1, 2).insert(0, 1).insert(2, 3)

    def test_dft(self):
        bst = BinarySearchTree(iter_type=DFIter)
        bst.insert(1, 2).insert(0, 1).insert(2, 3).insert(-1, 1)

    def test_contains(self):
        bst = BinarySearchTree()
        bst.insert(1, 2).insert(2, 3).insert(3, 4)

        self.assertTrue(1 in bst)
        self.assertFalse(9 in bst)

    def test_remove(self):
        bst = BinarySearchTree()
        bst.insert(1, 2).insert(0, 1).insert(2, 3)

        self.assertTrue(1 in bst)

        bst.remove(1)

        self.assertFalse(1 in bst)


if __name__ == '__main__':
    unittest.main()
