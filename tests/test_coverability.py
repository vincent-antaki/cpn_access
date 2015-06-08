#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import numpy as np
import petrinet as pn
from nose.tools import set_trace
from algorithms import coverable

#np.set_printoptions(threshold='nan')

class CoverabilityTest(unittest.TestCase):
    def setUp(self):
        self.solver = 'z3'

        self.a =  np.matrix([[(1, 0), (1, 3), (0, 1), (0, 0)],
                              [(1, 1), (2, 0), (0, 0), (1, 0)],
                              [(0, 2), (0, 1), (1, 0), (0, 1)]], dtype=[('pre', 'uint'), ('post', 'uint')])

        self.b = np.matrix([[(1, 2), (5, 6), (0,1), (7, 8), (9, 0)],
                            [(1, 2), (5, 6), (0,0), (7, 8), (9, 0)]], dtype=[('pre', 'uint'), ('post', 'uint')])
                            
        self.c = np.matrix([
    #  t1      t2      t3      t4      t5      t6      s1      s2      s3
    [(0, 1), (0, 0), (0, 0), (1, 0), (0, 0), (1, 0), (0, 0), (0, 0), (0, 0)],  # q1
    [(1, 0), (0, 1), (0, 0), (0, 0), (0, 1), (0, 0), (0, 0), (0, 0), (0, 0)],  # q2
    [(0, 0), (1, 0), (0, 1), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],  # q3
    [(0, 0), (0, 0), (1, 0), (0, 1), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],  # q4
    [(0, 0), (0, 0), (0, 0), (0, 0), (1, 0), (0, 1), (0, 0), (0, 0), (0, 0)],  # q5
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 1), (0, 0), (1, 0)],  # p1
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (1, 0), (0, 1), (0, 0)],  # p2
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (1, 0), (0, 1)],  # p3
    [(0, 0), (1, 1), (0, 0), (0, 0), (0, 0), (0, 0), (1, 0), (0, 0), (0, 1)],  # b1
    [(0, 0), (0, 0), (0, 0), (1, 1), (1, 0), (0, 0), (0, 1), (0, 0), (1, 0)],  # nb1
    [(0, 1), (0, 0), (1, 0), (0, 0), (0, 0), (1, 0), (0, 0), (1, 1), (0, 0)]], # nb2
    dtype=[('pre', 'int64'), ('post', 'int64')])
    
    
    def test_easy_coverable(self):
        
        m0 = np.array([1,1,0])
        m = np.array([15,1,10])
        
        z = coverable(self.a,m0,m,solver=self.solver)
        print(z)
        product = (np.dot(pn.incident(self.a),z) + m0).getA1()
#        print(product)
        self.assertTrue(all([product[i] >= m[i] for i in range(0,m0.size)]))
#        self.assertTrue(False)
        
    def test_easy_not_coverable(self):
        
        m0 = np.array([1,1,0])
        m = np.array([10,2,10])
        
        z = coverable(self.a,m0,m,solver=self.solver)
#        print(z)
        self.assertTrue(z is False)
#        self.assertTrue(False)

    def test_clearly_uncoverable(self):
        
        m = np.ones((self.c.shape[0],), dtype=np.int)
        m0 = np.zeros((self.c.shape[0],), dtype=np.int)
        
        z = coverable(self.c,m0,m,solver=self.solver)
#        print(z)
        self.assertTrue(z is False)
#        self.assertTrue(False)
        
    def test_already_covered(self):
        m0 = np.ones((self.c.shape[0],), dtype=np.int)
        m = np.zeros((self.c.shape[0],), dtype=np.int)

        z = coverable(self.c, m0, m, solver=self.solver)
#        print(z)
        self.assertTrue(z)
#        self.assertTrue(False)

    def test_not_coverable(self):


        pass

