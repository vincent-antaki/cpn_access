#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import numpy as np
import petrinet as pn

from petrinet import reversed_net
        
class TestMatrix(unittest.TestCase):
    def setUp(self):
        self.net = np.matrix([[(2, 0), (0, 0), (3, 8), (1, 2), (0,37), (0,0)],
                              [(0, 3), (1, 3), (5, 0), (5, 2), (23,0), (0,0)]],
                             dtype=[('pre', 'uint'), ('post', 'uint')])
        self.a = np.matrix(
           [[(1,0), (1,3), (0,1), (1,0)],
            [(1,1), (2,0), (0,0), (0,0)],
            [(0,0), (0,1), (1,0), (0,1)]],
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
        self.assertTrue(np.array_equal(pn.preset(self.net, [0,1], True),[0,1,2,3,4]))                
        self.assertTrue(np.array_equal(pn.preset(self.net, [0, 1, 2, 3, 4, 5]), [0, 1]))                
        self.assertTrue(np.array_equal(pn.preset(self.net, [1, 4]), [1]))                
 
    def test_postset(self) :
        self.assertTrue(np.array_equal(pn.postset(self.net, [0], True),[0,2,3]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [1], True),[1,2,3,4]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [0]),[1]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [2]),[0]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [3]),[0,1]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [4]),[0]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [5]),[]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [2,4]),[0]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [0,1]),[1]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [0,1,2,3,4]),[0,1]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [0,1], True),[0,1,2,3,4]))                

    def test_subnet(self):
        self.assertTrue(np.array_equal(pn.subnet(self.a,[0]),np.array([[(1,0)],[(1,1)],[(0,0)]],dtype=[('pre', 'uint'), ('post', 'uint')])))
        self.assertTrue(np.array_equal(pn.subnet(self.a,[0],True)[0],np.array([[(1,0)],[(1,1)]],dtype=[('pre', 'uint'), ('post', 'uint')])))        
        self.assertTrue(np.array_equal(pn.subnet(self.a,[2,3]),np.array([[(0,1),(1,0)],[(0,0),(0,0)],[(1,0),(0,1)]],dtype=[('pre', 'uint'), ('post', 'uint')])))        
        self.assertTrue(np.array_equal(pn.subnet(self.a,[2,3],True)[0],np.array([[(0,1),(1,0)],[(1,0),(0,1)]],dtype=[('pre', 'uint'), ('post', 'uint')])))                
        
    def test_reversed(self):
        net = np.matrix([[(1, 2), (3, 4)]], dtype=[('pre', 'uint'), ('post', 'uint')])

        rev = reversed_net(net)

        # reversed pre and post
        self.assertTrue(np.array_equal([[2, 4]], rev['pre']))
        self.assertTrue(np.array_equal([[2, 4]], net['post']))
        self.assertTrue(np.array_equal([[1, 3]], rev['post']))
        self.assertTrue(np.array_equal([[1, 3]], net['pre']))
        
#CopyPasta with rec.array instead of matrix
class TestRecArray(unittest.TestCase):
    def setUp(self):
        self.net = np.rec.array([[(2, 0), (0, 0), (3, 8), (1, 2), (0,37), (0,0)],
                              [(0, 3), (1, 3), (5, 0), (5, 2), (23,0), (0,0)]],
                             dtype=[('pre', 'uint'), ('post', 'uint')])
        self.a = np.rec.array(
           [[(1,0), (1,3), (0,1), (1,0)],
            [(1,1), (2,0), (0,0), (0,0)],
            [(0,0), (0,1), (1,0), (0,1)]],
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
        self.assertTrue(np.array_equal(pn.preset(self.net, [0,1], True),[0,1,2,3,4]))                
        self.assertTrue(np.array_equal(pn.preset(self.net, [0, 1, 2, 3, 4, 5]), [0, 1]))                
        self.assertTrue(np.array_equal(pn.preset(self.net, [1, 4]), [1]))                
 
    def test_postset(self) :
        self.assertTrue(np.array_equal(pn.postset(self.net, [0], True),[0,2,3]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [1], True),[1,2,3,4]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [0]),[1]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [2]),[0]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [3]),[0,1]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [4]),[0]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [5]),[]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [2,4]),[0]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [0,1]),[1]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [0,1,2,3,4]),[0,1]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [0,1], True),[0,1,2,3,4]))                

    def test_subnet(self):
        self.assertTrue(np.array_equal(pn.subnet(self.a,[0]),np.array([[(1,0)],[(1,1)],[(0,0)]],dtype=[('pre', 'uint'), ('post', 'uint')])))
        self.assertTrue(np.array_equal(pn.subnet(self.a,[0],True)[0],np.array([[(1,0)],[(1,1)]],dtype=[('pre', 'uint'), ('post', 'uint')])))        
        self.assertTrue(np.array_equal(pn.subnet(self.a,[2,3]),np.array([[(0,1),(1,0)],[(0,0),(0,0)],[(1,0),(0,1)]],dtype=[('pre', 'uint'), ('post', 'uint')])))        
        self.assertTrue(np.array_equal(pn.subnet(self.a,[2,3],True)[0],np.array([[(0,1),(1,0)],[(1,0),(0,1)]],dtype=[('pre', 'uint'), ('post', 'uint')])))                
        
    def test_reversed(self):
        net = np.rec.array([[(1, 2), (3, 4)]], dtype=[('pre', 'uint'), ('post', 'uint')])

        rev = reversed_net(net)

        # reversed pre and post
        self.assertTrue(np.array_equal([[2, 4]], rev['pre']))
        self.assertTrue(np.array_equal([[2, 4]], net['post']))
        self.assertTrue(np.array_equal([[1, 3]], rev['post']))
        self.assertTrue(np.array_equal([[1, 3]], net['pre']))

#CopyPasta with array instead of matrix

class TestArray(unittest.TestCase):
    def setUp(self):
        self.net = np.array([[(2, 0), (0, 0), (3, 8), (1, 2), (0,37), (0,0)],
                              [(0, 3), (1, 3), (5, 0), (5, 2), (23,0), (0,0)]],
                             dtype=[('pre', 'uint'), ('post', 'uint')])
        self.a = np.array(
           [[(1,0), (1,3), (0,1), (1,0)],
            [(1,1), (2,0), (0,0), (0,0)],
            [(0,0), (0,1), (1,0), (0,1)]],
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
        self.assertTrue(np.array_equal(pn.preset(self.net, [0,1], True),[0,1,2,3,4]))                
        self.assertTrue(np.array_equal(pn.preset(self.net, [0, 1, 2, 3, 4, 5]), [0, 1]))                
        self.assertTrue(np.array_equal(pn.preset(self.net, [1, 4]), [1]))                
 
    def test_postset(self) :
        self.assertTrue(np.array_equal(pn.postset(self.net, [0], True),[0,2,3]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [1], True),[1,2,3,4]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [0]),[1]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [2]),[0]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [3]),[0,1]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [4]),[0]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [5]),[]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [2,4]),[0]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [0,1]),[1]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [0,1,2,3,4]),[0,1]))
        self.assertTrue(np.array_equal(pn.postset(self.net, [0,1], True),[0,1,2,3,4]))                

    def test_subnet(self):
        self.assertTrue(np.array_equal(pn.subnet(self.a,[0]),np.array([[(1,0)],[(1,1)],[(0,0)]],dtype=[('pre', 'uint'), ('post', 'uint')])))
        self.assertTrue(np.array_equal(pn.subnet(self.a,[0],True)[0],np.array([[(1,0)],[(1,1)]],dtype=[('pre', 'uint'), ('post', 'uint')])))        
        self.assertTrue(np.array_equal(pn.subnet(self.a,[2,3]),np.array([[(0,1),(1,0)],[(0,0),(0,0)],[(1,0),(0,1)]],dtype=[('pre', 'uint'), ('post', 'uint')])))        
        self.assertTrue(np.array_equal(pn.subnet(self.a,[2,3],True)[0],np.array([[(0,1),(1,0)],[(1,0),(0,1)]],dtype=[('pre', 'uint'), ('post', 'uint')])))
        
    def test_reversed(self):
        net = np.array([[(1, 2), (3, 4)]], dtype=[('pre', 'uint'), ('post', 'uint')])

        rev = reversed_net(net)

        # reversed pre and post
        self.assertTrue(np.array_equal([[2, 4]], rev['pre']))
        self.assertTrue(np.array_equal([[2, 4]], net['post']))
        self.assertTrue(np.array_equal([[1, 3]], rev['post']))
        self.assertTrue(np.array_equal([[1, 3]], net['pre']))
