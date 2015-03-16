from scipy import optimize
from petrinet import *
import numpy as np
from fractions import Fraction
from decimals import Decimal
from nose.tools import set_trace

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
    
    
def reachable(net, m0, m, limreach=False, options = False):
    """
    Reachable algorithm from [FH13] - Section 4

    Input : 
        net : a continous petri net system, represented by a numpy reccord matrix with 2d tuples as elements
        m0 : an initial marking, represented by a 1-dimension numpy array
        m : a objective marking, represented by a 1-dimension numpy array
        limreach : if true, reachable will test the lim-reachability of marking m

        options : a dictionnary
            1.diagnosis : if linprog solver doesn't arrive at a solution for a resolution, verifies that a "complementary" problem has a solution (a.k.a Farka's lemma)
            2.callback : Use callback function to stop the simplex solver at the beginning of optimization phase (phase 2).
            3.proofcheck : Verify with symbolic computation 
    Output : 
        sol : False if not reachable, else returns Parikh Image of solution, represented by a 1d numpy array.
        
    """
    opts = {'diagnosis':True,'proofcheck':False,'callback':False}
    if options :
        for x in options.key:
            opts[x] = options[x]
    n1, n2   = net.shape

    assert len(m) == n1 and n1 == len(m0)

    if (m == m0).all() : 
        return [0 for x in range(0,n2)]
        
    t1 = np.array(range(0,n2)) #initialy, t1 represents all the transitions of the Petri net system
    b_eq = np.array(m - m0)
    
    while t1.size != 0:
        nbsol, sol, l  = 0,np.zeros(n2), t1.size #sol is initialize as a null vector        
        A_eq = incident(subnet(net,t1))

        for t in t1:
            objective_vector = [objective(t,x) for x in range(0,l)]
            
            if opts['callback'] :
            
                #Callback function, will be use to stop the simplex when it has a valid solution with xk[t] > 0
                def strict_positive_t(xk, **kwargs) :
                    print("strictpositive fct : xk = ",xk, xk[t]>0)
                    print(kwargs)
                    if kwargs["phase"] == 2 and xk[t] > 0 :
                        print("Found solution :",xk)
                        raise FoundSolution(xk)

                try :
                    #http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
                    #solve (exist v | v>=0 and C_{PxT1}v = m - m0)                          
                    print(t1, None)
                    print(t)
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
            else :
                    result = optimize.linprog(objective_vector, None, None, A_eq, b_eq)
                    if (result.status == 0 or result.status == 3) and result.x[t]>0:
                        nbsol += 1
                        sol += result.x
                    
            print("result for t=",t," :",result)

            if opts['proofcheck'] and (result.status == 3 or (result.status == 0 and result.x[t]>0)):
                #symbolic computaion here
                pass
            
            elif opts['diagnosis'] and (result.status == 2 or (result.status == 0 and result.x[t]==0)) :
                check = None
                #If this present section of code is executed, it implies that optimize.linprog was not able to find a feasable solution to the system
            
                """
                Considering Farka's lemma variants. For every unfeasable system of the shape : 
                    Ax = b such as x>=0 
                    
                The following system is feasable :
                    yA >= 0 (A^t y >= 0) and yb < 0
                    
                    yb is a negative scalar. By defining b as objective vector, the simplex will have the objective of minimising yb which is quite a nice objective to have when you want yb to be negative. Again, unless options.callback is False, a callback function will be sent to linprog to stop the iteration if a solution to the system with the extra constraint on yb is found.
                """
                objective_vector = b_eq
                print("b_eq (diagnosis objective) before transpose", objective_vector)
                bt = -1 *b_eq.transpose()
                print("after transpose", bt)
                
                if opts['callback'] :            
                
                    def strict_negative_yb(xk, **kwargs) :
                        if kwargs["phase"] == 2 and np.cdot(bt,xk) < 0 :
                            print("Found solution :",xk)
                            raise FoundSolution(xk)
                    try :                
                        check = optimize.linprog(objective_vector, None, None, A_eq.transpose() , [0 for i in range(0,l)], callback = strict_negative_yb)
                    except FoundSolution as f :
                        print("Found Diagnosis Solution and aborted the rest of the simplex", f.x)
                        break
                else :
                    check = optimize.linprog(objective_vector, None, None, A_eq.transpose() , [0 for i in range(0,l)])                 
                print("Check done. \n",check)
                    
                

        #The combination of the transitions cannot be equal de m-m0        
        if nbsol == 0 :
            print("No solution")
            return False

        else :
            sol *= 1/nbsol 

        t1 = sol.nonzero()[0] #Indexes of non-zero transitions (transitions that are fired)
        sub, subplaces = subnet(net, t1, True) 
        
        t1 = np.intersect1d(t1, maxFS(sub, m0.take(subplaces)),assume_unique=True)
        
        if not limreach:
            t1 = np.intersect1d(t1, maxFS(reversed_net(sub), m.take(subplaces)),assume_unique=True)
        print(t1)
        print(sol)
        print("t1 == sol.nonzero ",np.array(t1) == sol.nonzero())
        print("t1 == sol.nonzero all",(np.array(t1) == sol.nonzero()).all())        
        if (np.array(t1) == sol.nonzero()).all() :
            return sol

def objective(t,x):
    if t == x : return -1
    else : return 0

class FoundSolution(Exception):
    def __init__(self, solution):
        self.solution = solution

