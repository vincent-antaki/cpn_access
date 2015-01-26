import unittest

import PetriNet as pn
from nose.tools import set_trace 
from cpn_analysis import *

class PrePostsetTest(unittest.TestCase):

    def setUp(self):

        self.p = pn.PetriNet(
                ((1, 1, 0, 0), 
                (1, 2, 0, 1), 
                (0, 0, 1, 0)),
                
                ((0, 3, 1, 0), 
                (1, 0, 0, 0), 
                (2, 1, 0, 1)))

    def test_preset(self):
    
        self.assertTrue(np.array_equal(self.p.preset(1),[0,1]))
        self.assertTrue(np.array_equal(self.p.preset(3),[1]))
        self.assertTrue(self.p.preset(1, place=True) == [0])  

    def test_postset(self):

        self.assertTrue(np.array_equal(self.p.postset(0,True),[0,1]) )
        self.assertTrue(np.array_equal(self.p.postset(1,True),[0,1,3]))
        self.assertTrue(np.array_equal(self.p.postset(1,True),[0,1,3]))
        self.assertTrue(np.array_equal(self.p.postset(1),[0,2]))        
    
        
class CPNTest(unittest.TestCase):

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
        
#for config in apply_transition(net, config_init, trans):
 #   print config
        
 #   def test_fireable(self):
#        z = fireable(self.a,,)
        
        
        
#unittest.run()
