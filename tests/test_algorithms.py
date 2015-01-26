import unittest
import numpy as np

from algorithms import fireable

class FirableTest(unittest.TestCase):
    def test_empty_net(self):
        pass

    def test_sample(self):
        p = np.matrix([[(1, 0), (1, 3), (0, 1), (0, 0)],
                       [(1, 1), (2, 0), (0, 0), (1, 0)],
                       [(0, 2), (0, 1), (1, 0), (0, 1)]], dtype=[('pre', 'uint'), ('post', 'uint')])

        self.assertTrue(fireable(p, (1, 2, 3), [1, 2, 3]))
