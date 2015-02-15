import unittest
import numpy as np
import petrinet as pn
from nose.tools import set_trace
from algorithms import fireable, reachable

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
        #set_trace()
        pass

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
        #set_trace()
        print(self.a,self.a.dtype)
        z = reachable(self.a, m0, m)
        print(np.transpose(z))
        print(self.a,self.a.dtype)
        print("z : ", z)
        print(m0, "<- m0 . m ->", m)
        print("a incident :", pn.incident(self.a))
        print("numpy array :",(pn.incident(self.a)*np.array([[2],[1],[1],[0]])).getA1())
        print("normal array",(pn.incident(self.a)*[[2],[1],[1],[0]]).getA1())
        print("difference :",m - m0)
        self.assertTrue(np.array_equiv((pn.incident(self.a)*[[2],[1],[1],[0]]).getA1(), m - m0))
        #valid path from m0 to m : [1,0,2,3,2,0]. associated Parikh image : [2,1,2,1]


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
        self.assertTrue(not reachable(self.b,m0,m))
        self.assertTrue(reachable(self.a,m0,m))
        self.assertTrue(reachable(self.b,m0,m),limreach=True)


#last = list(apply_transition(n, c, t))[-1]
#for config in apply_transition(net, config_init, trans):
 #   print config

 #   def test_fireable(self):
#        z = fireable(self.a,,)

