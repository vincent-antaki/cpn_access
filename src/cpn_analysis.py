import numpy as np
import PetriNet


#v est un python array             
def supportvector(v):
    return np.array(v).nonzero()[0]
    
#takes in input : n, a petriNet instance; m, an initial marking; t1, an index subset of transitions of n 
# m is a numpy array
def fireable(n, m, t1):
    t2,p = np.empty((0,)), m.nonzero()[0]
    assert n.shape[0] == m.shape[0]

    while t2 != t1:
        new = False
        for t in np.setdiff1d(t1,t2) :
            if n.preset(t) in p :
                t2, p, new = t2.union1d(t), np.union1d(p,n.postset(t)), True
        if not new : return (False, t2)
    return (True,None)

#takes in input : n, a petriNet instance; m0, an initial marking; m, a marking 
#returns a tuple with (reachable?, Parikh image if reachable==true)

#m0 and m are considered to be a Python Array
def reachable(n, m0, m):
    if m == mo : return (True,0)
    t1 = n.trans.copy()
    while t1:
        nbsol, sol  = 0,np.zero(len(m0)) #sol est initialisé comme vecteur nul
        for t in t1:
            #solve (exist v | v>=0 and v[t]>0 and C_{PxT1}v = m - m0)
            ###insert solver here and assigne answer to v    
            
            if v : nbsol, sol =+ 1, v
        
        if nbsol == 0 : return False
        else : sol *= 1/nbsol
        
        t1 = set(sol.nonzero())
        ### to be continued...       
