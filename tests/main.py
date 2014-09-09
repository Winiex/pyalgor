import unittest


from algorithms.tree import BinarySearchTree


class TestBinarySearchTree(unittest.TestCase):

    def setUp(self):
        pass

    def test_insert(self):
        bst = BinarySearchTree()
        bst.insert(1, 2).insert(0, 1).insert(2, 3)

        for node in bst:
            print node


if __name__ == '__main__':
    unittest.main()
