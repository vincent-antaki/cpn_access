#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import numpy as np
import petrinet as pn
from nose.tools import set_trace
from algorithms import fireable, reachable

#np.set_printoptions(threshold='nan')

class FireableTest(unittest.TestCase):
    def setUp(self):
        self.a =  np.matrix([[(1, 0), (1, 3), (0, 1), (0, 0)],
                              [(1, 1), (2, 0), (0, 0), (1, 0)],
                              [(0, 2), (0, 1), (1, 0), (0, 1)]], dtype=[('pre', 'uint'), ('post', 'uint')])

        self.b = np.matrix([[(1, 2), (5, 6), (0,1), (7, 8), (9, 0)],
                            [(1, 2), (5, 6), (0,0), (7, 8), (9, 0)]], dtype=[('pre', 'uint'), ('post', 'uint')])


    def test_a(self):
        self.assertTrue(fireable(self.a, np.array((2, 7, 3)), np.array((0,1)))[0])
        self.assertTrue(fireable(self.a, np.array((2, 7, 3)), np.array((3)))[0])

        self.assertTrue(np.array_equal(fireable(self.a, np.array((2, 0, 1)), np.array([3]))[1],np.array([])))
        self.assertTrue(np.array_equal(fireable(self.a, np.array((1, 0, 3)), np.array([2,3]))[1],np.array([2])))


class ReachableTest(unittest.TestCase):
    def setUp(self):
        self.a = np.matrix(
               [[(1,0), (1,3), (0,1), (1,0)],
                [(1,1), (2,0), (0,0), (0,0)],
                [(0,0), (0,1), (1,0), (0,1)]],
        dtype=[('pre', 'uint'), ('post', 'uint')])

    def test_reachable(self):
        m0 = np.array((2, 7, 3))
        m = np.array((3, 5, 3))

        result = reachable(self.a, m0, m)
        #valid path from m0 to m : [1,0,2,0]. associated Parikh image : [2,1,1,0]
        z = result[np.newaxis].transpose()       

        self.assertTrue(np.array_equiv((pn.incident(self.a)*[[2],[1],[1],[0]]).getA1(), m - m0))
        self.assertTrue(np.array_equiv(np.dot(pn.incident(self.a),z).getA1(), m - m0))

    def test_unreachable(self):
        m0 = np.array((2, 7, 3))
        m = np.array((0, 0, 0))
        result = reachable(self.a, m0, m)
        self.assertTrue(result is False)

class LimReachTest(unittest.TestCase):
    def setUp(self):
        #a and b have the same incidence matrix but not the same reachable spaces
        #example took from On Reachability in Continuous Petri Net Systems by Julvez, Recalde and Silva
        self.a = np.matrix(
               [[(1,0), (0,1)],
                [(0,1), (1,0)]],
        dtype=[('pre', 'uint'), ('post', 'uint')])

        self.b = np.matrix(
               [[(2,1), (0,1)],
                [(0,1), (2,1)]],
        dtype=[('pre', 'uint'), ('post', 'uint')])

    def test_lim_difference(self):
        m0 = np.array([2,0])
        m = np.array([0,2])

        z = reachable(self.a,m0,m)
        self.assertIsInstance(z,np.ndarray)
        z = reachable(self.a, m0, m, limreach=True)
        self.assertIsInstance(z, np.ndarray)
                
        z = reachable(self.b,m0,m)
        self.assertTrue(z is False)        
        z = reachable(self.b, m0, m, limreach=True)
        self.assertIsInstance(z, np.ndarray)
        
class RecArrayLimReachTest(LimReachTest):
    def setUp(self):
        LimReachTest.setUp(self)
        self.a = np.rec.array(self.a)
        self.b = np.rec.array(self.b)
        print(self.a)
        print(self.b)
        
class RecArrayReachableTest(LimReachTest):
    def setUp(self):
        LimReachTest.setUp(self)
        self.a = np.rec.array(self.a)
        self.b = np.rec.array(self.b)
        print(self.a)
        print(self.b)        
