#!/usr/bin/python
# -*- coding: utf-8 -*-
import petrinet as pn
from algorithms import reachable, fireable
import numpy as np

petrinet = np.matrix([
        [(2, 0), (0, 0), (3, 8), (1, 2), (0,37)],
         [(0, 3), (1, 3), (5, 0), (5, 2), (23,0)]],
         dtype=[('pre', 'uint'), ('post', 'uint')])
         
a = np.matrix(
               [[(1,0), (1,3), (0,1), (1,0)],
                [(1,1), (2,0), (0,0), (0,0)],
                [(0,0), (0,1), (1,0), (0,1)]],
        dtype=[('pre', 'uint'), ('post', 'uint')])

#matrix([[-1,  2,  1, -1],
#        [ 0, -2,  0,  0],
#        [ 0,  1, -1,  1]])

b = np.matrix([
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

solver = 'scipy'

def test_reachable1():
    m0 = np.array((2, 7, 3))
    m = np.array((3, 5, 3))

    result = reachable(a, m0, m,solver=solver)
    #valid path from m0 to m : [1,0,2,0]. associated Parikh image : [2,1,1,0]
    z = result[np.newaxis].transpose()       

    assert (np.array_equiv((pn.incident(a)*[[2],[1],[1],[0]]).getA1(), m - m0))
    assert (np.array_equiv(np.dot(pn.incident(a),z).getA1(), m - m0))

def test_reachable2():

    m0 = np.array([1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1])

    #print(reachable(b, m0, np.array([0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0], dtype='int64'),solver=solver))
    

    
    #t6 is a valid path
    m = np.array([0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0], dtype='int64')
    z = reachable(b, m0,m,solver=solver)
    print(z)
    print(np.dot(pn.incident(b),z[np.newaxis].transpose()))
    print(m-m0)
    assert (np.array_equiv(np.dot(pn.incident(b),z[np.newaxis].transpose()).getA1()
            , m-m0))
    #t6, t5 is a valid path
    
    m = np.array([0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0])
    z = reachable(b, m0, m, solver=solver)
    assert (np.array_equiv(np.dot(pn.incident(b),z[np.newaxis].transpose()).getA1()
            , m-m0))        
    #t6t5t1 is a valid path
    m = np.array([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
    z = reachable(b, m0, m, solver=solver)
    assert (np.array_equiv(np.dot(pn.incident(b),z[np.newaxis].transpose()).getA1()
            , m-m0))        

    #t6t5t1t6
    
    m = np.array([0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0])
    
    z = reachable(b, m0, m, solver=solver)
    assert (np.array_equiv(np.dot(pn.incident(b),z[np.newaxis].transpose()).getA1()
            , m-m0))        

test_reachable1()
test_reachable2()

#print("net:", petrinet)
#print("preset:", pn.preset(petrinet, [2]))
#print("postset:", pn.postset(petrinet, [1]))
#print("reversed", pn.reversed_net(petrinet))
#print("subnet:", pn.subnet(petrinet, [1, 3]))
#print("subnet:", pn.subnet(petrinet, [1, 3], True))
