#!/usr/bin/python
# -*- coding: utf-8 -*-
from petrinet import *
import numpy as np
from fractions import Fraction
import qsoptex

"""
Fireable and Reachable algorithms from : 

[FH13] - Fraca and Haddad, Complexity Analysis of Continous Petri Net.

"""
def fireable(net, m, t1):
    """
    Fireable algorithm from [FH13] - Section 3

    Input : 
        net : a continous petri net system, represented by a numpy reccord matrix with 2d tuples as elements
        m : an initial marking, represented by a 1-dimension numpy array
        t1 : an numpy array of ordered indexes reprensenting a subset of the net's transitions

    Output : (fireable?, t2)
        fireable? : a boolean that indicates if all t1 can be fired
        t2 : returns the maximal firing set include in t1 (if fireable == true => t1 == t2)
                
    """
    assert net.shape[0] == m.shape[0]
    t2,p = np.empty((0,)), m.nonzero()[0]
    
    while np.setdiff1d(t1,t2).size != 0:
        new = False
        for t in np.setdiff1d(t1,t2) :
            if all(np.in1d(preset(net, [t]),p,assume_unique=True)) :
                t2, p, new = np.union1d(t2,[t]), np.union1d(p, postset(net, [t])), True
        if not new : return (False, t2)
    return (True,t2)
    
def maxFS(net, m):
    """
    Calls Fireable with all the transitions of the net. Returns only t2 (the maximal firing set)
    """
    return fireable(net,m, np.array(range(0,net.shape[1])))[1]    
#    return fireable(net,m,np.zeros((1,net.shape[1])))[1]    
    
    
def reachable(net, m0, m, limreach=False):
    """
    Reachable algorithm from [FH13] - Section 4

    Input : 
        net : a continous petri net system, represented by a numpy reccord matrix with 2d tuples as elements
        m0 : an initial marking, represented by a 1-dimension numpy array
        m : a final marking, represented by a 1-dimension numpy array
        limreach : if true, reachable will test the lim-reachability of marking m

    Output : 
        sol : False if not reachable, else returns Parikh Image of solution, represented by a 1d numpy array.
        
    """
    n1, n2 = net.shape
    assert len(m) == n1 and n1 == len(m0)
    
    #initialy, t1 represents all the transitions of the Petri net system
    t1 = np.array(range(0,n2))

    if np.array_equiv(m,m0) : 
        return [0 for x in t1] 
        
    b_eq = np.array(m - m0)
    
    while t1.size != 0:
        l = t1.size
        nbsol, sol = 0,np.zeros(l,dtype=Fraction)  
        A_eq = incident(subnet(net,t1))

        for t in t1:
            objective = [minus_one_if_equal(t,x) for x in range(0,l)]         
            result = solve_qsopt(objective, A_eq, b_eq, t)
            if result is not None :
                nbsol += 1
                sol += result        
        
        if nbsol == 0 :
            #No solution, there is no combination of the transitions cannot be equal de m-m0.
            print("No solution")
            return False 

        else :
            # in numpy, sol *= 1/nbsol cast sol in float
            # and we do not want that to happen.
            y = Fraction(1,nbsol)
            sol = [x * y for x in list(sol)]
            sol = np.array(sol,dtype=Fraction) 
            
        t1 = sol.nonzero()[0]
        sub, subplaces = subnet(net, t1, True) 
        t1 = np.intersect1d(t1, maxFS(sub, m0.take(subplaces)),assume_unique=True)
        
        if not limreach:
            t1 = np.intersect1d(t1, maxFS(reversed_net(sub), m.take(subplaces)),assume_unique=True)

        if np.array_equiv(t1,sol.nonzero()) :
            #Found a solution. yay.
            return sol

    return False

class FoundSolution(Exception):
    def __init__(self, solution):
        self.solution = solution
    
def minus_one_if_equal(t,x):
    if t == x : return -1
    else : return 0

def one_if_equal(t,x):
    if t == x : return 1
    else : return 0

#e is the index of the strict probability constraint.
def solve_qsopt(c, A, b, e):
    r = solve_with_qsopt(c, A, b)    

    if r.status == qsoptex.SolutionStatus.INFEASIBLE or (r.status == qsoptex.SolutionStatus.OPTIMAL and r.x[e] == 0):
        #QSopt_ex : INFEASABLE
        return None
                
    elif r.status == qsoptex.SolutionStatus.UNBOUNDED :
        #QSopt_ex : UNBOUNDED
        d = [0 for x in c]
        
        A_up = np.array([[one_if_equal(i,e) for i, x in enumerate(c)]])
        b_up = [1] #this is an arbitrairy cut
        r = solve_with_qsopt(d, A, b, A_up, b_up)
                    
    assert r.status == qsoptex.SolutionStatus.OPTIMAL
    return r.x 
    
    
def solve_with_qsopt(c, A_eq, b_eq, A_up=None, b_up=None, objective=qsoptex.ObjectiveSense.MINIMIZE):
    """Solve using arbitrary precision floats"""
    assert A_eq.shape[0] == len(b_eq)
    
    p = qsoptex.ExactProblem()
    names = []
    n = len(c)
    
    for i, x in enumerate(c):
        names.append(bytes([i]))
        p.add_variable(name=names[i],objective=x,lower=0)

    for index, line in enumerate(A_eq) :
        d = {} # dictionnary representing the constraint
        for x in range(0, n):
            d[x] = int(line.getA1()[x])

        p.add_linear_constraint(qsoptex.ConstraintSense.EQUAL, d, int(b_eq[index]))
        
        
    if A_up is not None and b_up is not None :
        assert A_up.shape[0] == len(b_up)
        for index, line in enumerate(A_up) :
            d = {} # dictionnary representing the constraints
            flat = line.flatten()
            for x in range(0, n):
                d[x] = int(flat[x])

            p.add_linear_constraint(qsoptex.ConstraintSense.GREATER, d, int(b_up[index]))
        
    p.set_objective_sense(objective)
    p.set_param(qsoptex.Parameter.SIMPLEX_DISPLAY, 0)
    p.set_param(qsoptex.Parameter.SIMPLEX_MAX_ITERATIONS,1)
    result = Bunch(status=p.solve(),x=[])

    if result.status == qsoptex.SolutionStatus.OPTIMAL :
        # récupération de la valeur de la solution
        for j in range(0, n):
            result.x.append(p.get_value(names[j]))
        
    return result

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def __str__(self):
        return str(self.__dict__)
