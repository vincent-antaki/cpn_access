from scipy import optimize
from petrinet import *
import numpy as np
from nose.tools import set_trace
"""
Algorithms from : 

[FH13] - Fraca and Haddad, Complexity Analysis of Continous Petri Net.

"""
def fireable(net, m, t1):
    """
    Fireable algorithm from [FH13] - Section 3

    Input : 
        net : a continous petri net system, represented by a numpy reccord matrix with 2d tuples as elements
        m : an initial marking, represented by a 1-dimension numpy array
        t1 : an array of ordered indexes reprensenting a subset of the net's transitions

    Output : (fireable?, t2)
        fireable? : a boolean that indicates if all t1 can be fired
        t2 : returns the maximal firing set include in t1 (if fireable == true => t1 == t2)
                
    """
    t2,p = np.empty((0,)), m.nonzero()[0]
    t1 = np.array(t1)
    assert net.shape[0] == m.shape[0]

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
    return fireable(net,m,range(0,net.shape[1]))[1]    
    
    
def reachable(net, m0, m, limreach=False):
    """
    Reachable algorithm from [FH13] - Section 4

    Input : 
        net : a continous petri net system, represented by a numpy reccord matrix with 2d tuples as elements
        m0 : an initial marking, represented by a 1-dimension numpy array
        m : a objective marking, represented by a 1-dimension numpy array
        limreach : if true, reachable will test the lim-reachability of marking m

    Output : 
        sol : False if not reachable, else returns Parikh Image of solution, represented by a 1d numpy array.
        
    """
    n1, n2   = net.shape

    assert len(m) == n1 and n1 == len(m0)

    if (m == m0).all() : 
        return (True,0)
        
    t1 = np.array(range(0,n2)) #initialy, t1 represents all the transitions of the Petri net system
    b_eq = np.array(m - m0)
    
    while t1.size != 0:
        nbsol, sol, l  = 0,np.zeros(n2), len(t1) #sol is initialize as a null vector        
        A_eq = incident(subnet(net,t1))

        for t in t1:
            objective_vector = [objective(t,x) for x in range(0,n2)]
            
            #Callback function, will be use to stop the simplex when it has a valid solution with xk[t] > 0
            def strict_positive_t(xk, **kwargs) :
                 if kwargs["phase"] == 2 and xk[t] > 0 :
                     print("Found solution :",xk)
                     raise FoundSolution(xk)

            try :
                #http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
                #solve (exist v | v>=0 and C_{PxT1}v = m - m0)
                print(objective_vector)
                print(None)
                print(A_eq)
                print(None) 
                print(b_eq) 
                result = optimize.linprog(objective_vector, None, None, A_eq, b_eq, callback = strict_positive_t)

            except FoundSolution as f :
                nbsol += 1
                sol += f.solution
                break

        if nbsol == 0 :
            return False
        else :
            sol *= 1/nbsol

        t1 = sol.nonzero()[0]
        sub, subplaces = subnet(net, t1, True)
        
        t1 = np.intersect1d(t1, maxFS(sub, m0.take(subplaces)),assume_unique=True)

        if not limreach:
            t1 = np.intersect1d(t1, maxFS(reversed_net(sub), m.take(subplaces)),assume_unique=True)

        if (t1 == sol.nonzero()).all() :
            return sol

def objective(t,x):
    if t == x : return -1
    else : return 0

class FoundSolution(Exception):
    def __init__(self, solution):
        self.solution = solution

