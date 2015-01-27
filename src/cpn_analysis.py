import numpy as np
from scipy import optimize
from nose.tools import set_trace 

import PetriNet

def maxFS(n, m):
    #set_trace()
    fire, vector = fireable(n,m,range(0,n.shape[1]))
    print(f)
    return f


#takes in input :
#n, a petriNet instance; 
#m, a numpy array representing an initial marking; 
#t1, an array of ordered index representing a subset of transitions of n 
#
def fireable(n, m, t1):
    set_trace()
    t2,p = np.empty((0,)), m.nonzero()[0]
    t1 = np.array(t1)
    assert n.shape[0] == m.shape[0]

    while np.setdiff1d(t1,t2).size != 0: 
        new = False
        for t in np.setdiff1d(t1,t2) :
            if all(np.in1d(n.preset(t),p,assume_unique=True)) :
                t2, p, new = np.union1d(t2,[t]), np.union1d(p,n.postset(t)), True
        if not new : return False, t2
    return True, None

#takes in input : n, a petriNet instance; m0, an initial marking; m, a marking 
#returns False if not reachable, returns Parikh Image if reachable
#m0 and m are considered to be a numpy arrays
def reachable(n, m0, m, limreach=False):
    n1, n2   = n.shape
        
    assert len(m) == n1 and n1 == len(m0)

    if (m == m0).all() : return (True,0)
    t1 = np.array(range(0,n2)) #initialy, t1 represents all the transitions of the petri net n
    b_eq = np.array(m - m0)
    print("initial marking : ", m0, " objective marking : ", m )
    print("objective : ", b_eq)
    while t1.size != 0:
    
        nbsol, sol, l  = 0,np.zeros(n2), len(t1) #sol est initialisé comme vecteur nul         
        A_eq = n.subnet(t1).incidenceMatrix()
        #b_up = np.zeros(l)
        #A_up = np.identity(l)  
               
        for t in t1:            
            objective_vector = [objective(t,x) for x in range(0,n2)]

            def strict_positive_t(xk, **kwargs) :
                 if kwargs["phase"] == 2 and xk[t] > 0 : 
                     raise FoundSolution(xk)
       
            try :                                           
                #http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html        
                #solve (exist v | v>=0 and v[t]>0 and C_{PxT1}v = m - m0)            
                print(A_eq,"/n",b_eq)
                result = optimize.linprog(objective_vector, None, None, A_eq, b_eq, callback = strict_positive_t)
                print(result)
            
                #if v[t]==0
            
            except FoundSolution as f :
                nbsol += 1
                print(f.solution)
                #set_trace()
                sol += f.solution
                break
        #set_trace()            
        print(nbsol)
        if nbsol == 0 :
            return False
        else :
            sol *= 1/nbsol
        
        t1 = sol.nonzero()
        sub, subplaces = n.subnet(t1, True)
        t1 = np.intersect1d(t1, maxFS(sub, m0.take(subplaces)),assume_unique=True)

        if limreach:
            t1 = np.insersect1d(t1, maxFS(sub, m.take(subplaces)),assume_unique=True)

        if t1 == sol.nonzero() : 
            return sol
            
def objective(t,x):
    if t == x : return -1
    else : return 0

class FoundSolution(Exception):
    def __init__(self, solution):
        self.solution = solution

