import unittest

from algorithms.tree import RBTree


class TestRBTree(unittest.TestCase):

    def setUp(self):
        pass

    def test_insert(self):
        rbt = RBTree()
        rbt.insert(0, 1).insert(1, 1).insert(2, 1)

        for node in rbt:
            pass


if __name__ == '__main__':
    unittest.main()
