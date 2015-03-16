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
        result = reachable(self.a, m0, m)
        expected_result = np.array([[2],[1],[1],[0]])
        expected_float = np.array([[2.0],[1.0],[1.0],[0.0]])
        #valid path from m0 to m : [1,0,2,0]. associated Parikh image : [2,1,1,0]
        z = result[np.newaxis].transpose()       
        print(self.a,self.a.dtype)
        print("result :", result, "\nz z.ndim z.shape: ", z,z.ndim, z.shape, z.dtype)
        print("expected result :", expected_result,expected_result.ndim,expected_result.shape, expected_result.dtype)
        print("the assert that fails\n","input 1 :",(pn.incident(self.a)*z).getA1(),"\n input 1 sans A1",pn.incident(self.a)*expected_result,"\n input 2 :", m-m0)
        print(m0, "<- m0 . m ->", m)
        print("expected_result and dimensions :",expected_result,expected_result.ndim )
        print("a incident :", pn.incident(self.a))
        print("normal array",(pn.incident(self.a)*z))
        print("np flat",(pn.incident(self.a)*z).getA1())
        print("dot",(np.dot(pn.incident(self.a),z)))        
        print("dot flat",(np.dot(pn.incident(self.a),z)).getA1())        
        print("difference :",m - m0)

        def alltest(a,e) :
            print("0",np.array_equiv(a,expected_result))
            print("1",np.array_equal(a,expected_result))                
            print("2",np.array_equiv(a.transpose(),expected_result))
            print("3",np.array_equal(a.transpose(),expected_result))
            print("4",np.array_equiv(a.transpose(),expected_result.transpose()))
            print("5",np.array_equal(a.transpose(),expected_result.transpose()))

        alltest(z,expected_result)
        alltest(z,expected_float)

        a =z.copy()
        e = expected_result.copy()        
        e = np.reshape(e, e.size)

        alltest(z,e)
        
        a = np.reshape(a,a.size)
        
        alltest(a,e)        
        alltest(a,expected_result)


        def alltest2(c, dot=True):
            print("a",np.array_equiv((pn.incident(self.a)*c), m - m0))
            print("b",np.array_equal((pn.incident(self.a)*c), m - m0))

            print("c",np.array_equiv((pn.incident(self.a)*c).getA1(), m - m0))
            print("d",np.array_equal((pn.incident(self.a)*c).getA1(), m - m0))

        alltest2(z)
        #alltest2(a)
        alltest2([[2],[1],[1],[0]])
        alltest2(expected_result)
        #alltest2(e)
        
        #self.assertTrue(np.array_equiv(a,expected_result))
 
        self.assertTrue(np.array_equiv((pn.incident(self.a)*[[2],[1],[1],[0]]).getA1(), m - m0))
        self.assertTrue(np.array_equiv(np.dot(pn.incident(self.a),z).getA1(), m - m0))

class UnreachableTest(unittest.TestCase):
    def setUp(self):
        self.a = np.matrix(
               [[(1,0), (1,3), (0,1), (1,0)],
                [(1,1), (2,1), (0,0), (0,0)],
                [(0,0), (0,1), (1,0), (0,1)]],
        dtype=[('pre', 'uint'), ('post', 'uint')])

    def test_reachable(self):
        m0 = np.array((2, 7, 3))
        m = np.array((0, 0, 0))
        #set_trace()
        result = reachable(self.a, m0, m)
        expected_result = False
        print(m0, "<- m0 . m ->", m)
        print("difference :",m - m0)
        self.assertTrue(np.array_equiv(z,expected_result))
        self.assertTrue(False)

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

