from unittest import TestCase

from PetriNet import *

class PresetTest(TestCase):

    def setUp(self):
        self.pre = ((1, 1, 0, 0), 
                (1, 2, 0, 1), 
                (0, 0, 1, 0))
                
        self.post = ((0, 3, 1, 0), 
                (1, 0, 0, 0), 
                (2, 1, 0, 1))

    def test_preset(self):
        p = PetriNet(pre, post)    
        self.assertTrue(np.array_equal(p.preset(1),[0,1]))
        self.assertTrue(np.array_equal(p.postset(1),[0,2]))
        self.assertTrue(np.array_equal(p.preset(3),[1]))
        self.assertTrue(p.preset(1, place=True) == [0]  )  
        self.assertTrue(np.array_equal(p.postset(0,True),[0,1]) )
        self.assertTrue(np.array_equal(p.postset(1,True),[0,1,3]))
        self.assertTrue(np.array_equal(p.postset(1,True),[0,1,3]))
