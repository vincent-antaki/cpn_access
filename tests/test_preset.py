import unittest
import PetriNet as pn
import numpy as np
import petrinet as apn
from nose.tools import set_trace 



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
    
class RecTest(unittest.TestCase):


    def setUp(self):
        self.net = np.matrix([
         [(2, 0), (0, 0), (3, 8), (1, 2), (0,37), (0,0)],
         [(0, 3), (1, 3), (5, 0), (5, 2), (23,0), (0,0)]],
         dtype=[('pre', 'uint'), ('post', 'uint')])

    def test_preset(self):
        #set_trace()
        print(apn.preset(self.net,[0]))
        print(np.array_equal(apn.preset(self.net, [0]),[0]))
        
        self.assertTrue(np.array_equal(apn.preset(self.net, [0]),[0]))    
        self.assertTrue(np.array_equal(apn.preset(self.net, [0, 1]),[0, 1]))
        
        self.assertTrue(np.array_equal(apn.preset(self.net, [0, 5]),[0]))    
        print(apn.preset(self.net, [0, 1, 2, 3, 4, 5]))
        self.assertTrue(np.array_equal(apn.preset(self.net, [0, 1, 2, 3, 4, 5]), [0, 1]))    
        
            
        self.assertTrue(np.array_equal(apn.preset(self.net, [1]),[1]))
        self.assertTrue(np.array_equal(apn.preset(self.net, [2]),[0,1]))
        self.assertTrue(np.array_equal(apn.preset(self.net, [3]),[0,1]))
        self.assertTrue(np.array_equal(apn.preset(self.net, [4]),[1]))
        self.assertTrue(np.array_equal(apn.preset(self.net, [5]),[]))        
        self.assertTrue(np.array_equal(apn.preset(self.net, [0], True),[2,3,4]))        
        self.assertTrue(np.array_equal(apn.preset(self.net, [1], True),[0,1,3]))
        
    def test_postset(self) :     
        
        self.assertTrue(np.array_equal(apn.postset(self.net, [0], True),[0,2,3]))        
        self.assertTrue(np.array_equal(apn.postset(self.net, [1], True),[1,2,3,4]))
        self.assertTrue(np.array_equal(apn.postset(self.net, [0]),[1]))
        self.assertTrue(np.array_equal(apn.postset(self.net, [2]),[0]))
        self.assertTrue(np.array_equal(apn.postset(self.net, [3]),[0,1]))
        self.assertTrue(np.array_equal(apn.postset(self.net, [4]),[0]))
        self.assertTrue(np.array_equal(apn.postset(self.net, [5]),[]))
        
        
#unittest.run()
