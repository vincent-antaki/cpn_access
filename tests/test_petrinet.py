import unittest
import numpy as np
import petrinet as pn

from petrinet import reversed_net

class TestReversed(unittest.TestCase):

    def test_reversed(self):
        net = np.array([[(1, 2), (3, 4)]], dtype=[('pre', 'uint'), ('post', 'uint')])

        rev = reversed_net(net)

        # reversed pre and post
        self.assertTrue(np.array_equal([[2, 4]], rev['pre']))
        self.assertTrue(np.array_equal([[1, 3]], rev['post']))

class TestPreset(unittest.TestCase):
    def setUp(self):
        self.net = np.matrix([[(2, 0), (0, 0), (3, 8), (1, 2), (0,37), (0,0)],
                              [(0, 3), (1, 3), (5, 0), (5, 2), (23,0), (0,0)]],
                             dtype=[('pre', 'uint'), ('post', 'uint')])

    def test_preset(self):
        self.assertTrue(np.array_equal(pn.preset(self.net, [0]),[0]))
        self.assertTrue(np.array_equal(pn.preset(self.net, [1]),[1]))
        self.assertTrue(np.array_equal(pn.preset(self.net, [2]),[0,1]))
        self.assertTrue(np.array_equal(pn.preset(self.net, [3]),[0,1]))
        self.assertTrue(np.array_equal(pn.preset(self.net, [4]),[1]))
        self.assertTrue(np.array_equal(pn.preset(self.net, [5]),[]))
        self.assertTrue(np.array_equal(pn.preset(self.net, [0], True),[2,3,4]))
        self.assertTrue(np.array_equal(pn.preset(self.net, [1], True),[0,1,3]))

class TestPostset(unittest.TestCase):
    def setUp(self):
        self.net = np.matrix([[(2, 0), (0, 0), (3, 8), (1, 2), (0,37), (0,0)],
                              [(0, 3), (1, 3), (5, 0), (5, 2), (23,0), (0,0)]],
                             dtype=[('pre', 'uint'), ('post', 'uint')])

    def test_postset(self) :
        self.assertTrue(np.array_equal(pn.postset(self.net, [0], True),[0,2,3]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [1], True),[1,2,3,4]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [0]),[1]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [2]),[0]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [3]),[0,1]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [4]),[0]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [5]),[]))
