import unittest
import numpy as np

from petrinet import reversed_net

class TestReversedNet(unittest.TestCase):
    def test_reversed(self):
        net = np.array([[(1, 2), (3, 4)]], dtype=[('pre', 'uint'), ('post', 'uint')])

        rev = reversed_net(net)

        # reversed pre and post
        self.assertTrue(np.array_equal([[2, 4]], rev['pre']))
        self.assertTrue(np.array_equal([[1, 3]], rev['post']))


