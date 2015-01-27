import unittest
import PetriNet as pn
import numpy as np
import petrinet as apn
from nose.tools import set_trace 

class FireableTest(unittest.TestCase):
    def setUp(self):
        self.a = pn.PetriNet(
                ((1, 1, 0, 1), 
                (1, 2, 0, 0), 
                (0, 0, 1, 0)),
                
                ((0, 3, 1, 0), 
                (1, 0, 0, 0), 
                (0, 1, 0, 1)))


    def test_empty_net(self):
        pass
        
    def test_simple(self):
    
        self.assertTrue(fireable(self.a, np.array((2, 7, 3)), np.array((0,1))))
        self.assertTrue(fireable(self.a, np.array((2, 7, 3)), np.array([3])))
        
        self.assertTrue(np.array_equal(fireable(self.a, np.array((2, 0, 1)), np.array([3])),(np.array([]))))        
        self.assertTrue(np.array_equal(fireable(self.a, np.array((1, 0, 3)), np.array([2,3])),(np.array([2]))))        

        
class ReachableTest(unittest.TestCase):

    def setUp(self):
        self.a = pn.PetriNet(
                ((1, 1, 0, 1), 
                (1, 2, 0, 0), 
                (0, 0, 1, 0)),
                
                ((0, 3, 1, 0), 
                (1, 0, 0, 0), 
                (0, 1, 0, 1)))

    def test_reachable(self):
        m0 = np.array((2, 7, 3))
        m = np.array((3, 5, 3)) 
        #set_trace()
        print((self.a.incidenceMatrix()*[[2],[1],[1],[0]]).getA1(), m - m0)     
        z = reachable(self.a, m0, m) 
        
        self.assertTrue(np.array_equiv((self.a.incidenceMatrix()*[[2],[1],[2],[1]]).getA1(), m - m0))
        #valid path from m0 to m : [1,0,2,3,2,0]. associated Parikh image : [2,1,2,1]
        self.assertTrue(z)
        
        #last = list(apply_transition(n, c, t))[-1]

