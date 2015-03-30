#!/usr/bin/python
# -*- coding: utf-8 -*-
from scipy import optimize
from petrinet import *
import numpy as np
import collections
from fractions import Fraction
import qsoptex
import math




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
    print(m, m.shape,"a", net, net.shape)
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
#    return fireable(net,m,np.zeros((1,net.shape[1])))[1]    
    
    
def reachable(net, m0, m, limreach=False, **options):
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
    opts = {'method': None,'diagnosis':False,'proofcheck':True,'callback':False}
    for x in options.keys():
        opts[x] = options[x]
    n1, n2   = net.shape

    assert len(m) == n1 and n1 == len(m0)

    if np.array_equiv(m,m0) : 
        return [0 for x in range(0,n2)]
        
    t1 = np.array(range(0,n2)) #initialy, t1 represents all the transitions of the Petri net system
    b_eq = np.array(m - m0)
    
    while t1.size != 0:
        l = t1.size
        nbsol, sol = 0,np.zeros(l,dtype=Fraction)  
        A_eq = incident(subnet(net,t1))

        for t in t1:
            objective_vector = [objective(t,x) for x in range(0,l)]
            result = None
            check = None
            
            if opts['method'] == 'Scipy' or opts['method'] == None:
           
                if opts['callback'] :
                    result = solve_lineprog_with_callback(objective_vector, A_eq, b_eq,lambda x : x[t] >0)
                
                else :
                    # à défaut d'avoir un callback, rajouter options = {maxiter:1}? 
                    result = solve_linprog(objective_vector, A_eq, b_eq, t)
                        
                print("Scipy's status : ",result.status, ", Scipy's answer : ",result.x )
                 
                if opts['proofcheck'] and (result.status == 3 or (result.status == 0 and result.x[t]>0)):
                    #symbolic computation here
                    s = cutFloat(result.x) #cutFloat approximate the represented float and return rationnal array.
                    if np.array_equiv(np.dot(A_eq,s[np.newaxis].transpose()).getA1(), b_eq) :
                        nbsol += 1
                        sol += s   
                    else : 
                        result = None                        
                
                elif opts['diagnosis'] and (result.status == 2 or (result.status == 0 and result.x[t]==0)) :          
                    #If this present section of code is executed, it implies that optimize.linprog was not able to find a feasable solution to the system
                    """
                    Considering Farka's lemma variants. For every unfeasable system of the shape : 
                        Ax = b such as x>=0 
                        
                    The following system is feasable :
                        yA >= 0 (A^t y >= 0) and yb < 0
                        
                        yb is a negative scalar. By defining b as objective vector, the simplex will have the objective of minimising yb which is quite a nice objective to have when you want yb to be negative. Again, unless options.callback is False, a callback function will be sent to linprog to stop the iteration if a solution to the system with the extra constraint on yb is found.
                    """
                    objective_vector = b_eq
                    bt = -1 *b_eq.transpose()

                    if opts['callback'] :
                        check = solve_lineprog_with_callback(objective_vector, A_eq.transpose(), [0 for i in range(0,l)],lambda x : np.cdot(-1 *b_eq.transpose(),x) < 0)
                    else :
                     # à défaut d'avoir un callback, rajouter options = {maxiter:1}? 
                        check = solve_linprog(objective_vector, A_eq.transpose(), [0 for i in range(0,l)])
                    print("Check done. \n",check)
                    
            if opts['method']=='QSopt_ex' or (opts['method'] == None and result == None):
                print("Solving with QSpot_ex...")
                result = solve_qsopt(objective_vector, A_eq, b_eq, t)
                if result is not None :
                    nbsol += 1
                    sol += result        

            print("result for t=",t," :",result)

        print("sol[0] type", type(sol[0]))
        print(list(sol))
        print(nbsol)
        #The combination of the transitions cannot be equal de m-m0        
        if nbsol == 0 :
            print("No solution")
            return False

        else :
            # sol *= 1/nbsol cannot do this with numpy because it cast sol in float 
            y = Fraction(1,nbsol)
            sol = [x * y for x in list(sol)]
            sol = np.array(sol,dtype=Fraction) #LOL. dat ghetto-fix.
            
        print("sol[0] type", type(sol[0]))
        t1 = sol.nonzero()[0] #Indexes of non-zero transitions (transitions that are fired)
        sub, subplaces = subnet(net, t1, True) 
        print("t1",t1, "\nnet", net, "\nsubplaces", subplaces)
        t1 = np.intersect1d(t1, maxFS(sub, m0.take(subplaces)),assume_unique=True)
        
        if not limreach:
            t1 = np.intersect1d(t1, maxFS(reversed_net(sub), m.take(subplaces)),assume_unique=True)
 #      if (np.array(t1) == sol.nonzero()).all() :
        if np.array_equiv(t1,sol.nonzero()) :
            print("entered t1 == sol.nonzero")
            return sol
    return False

def objective(t,x):
    if t == x : return -1
    else : return 0

def minus_one_if_equal(t,x):
    if t == x : return -1
    else : return 0

def one_if_equal(t,x):
    if t == x : return 1
    else : return 0

def cutFloat(x) :
    """convert x, a float or a float array, to a rationnal number (or a rationnal number array) by bounding its denominator. I know is a pretty bad heuristic for convertion but still cuts some cases"""
    if isinstance(x, float):
        return Fraction(x).limit_denominator(10000 * int(math.log10(x)))
    if isinstance(x, collections.Iterable):
        r = []
        for i in x :
            if i != 0 :
               denom = 10000 * math.ceil(math.log10(i))
               if denom >= 1 :
                   r.append(Fraction(i).limit_denominator(denom))
               else :
                   r.append(Fraction(i).limit_denominator(10000))
            else :
                r.append(Fraction(0))
        return np.array(r)

class FoundSolution(Exception):
    def __init__(self, solution):
        self.solution = solution

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def __str__(self):
        return str(self.__dict__)

"""
Following solvers solve a non-negative solution for the system Ax = b with strict inequalty on one element (refered as e) and nonnegativity on each element.
"""

def solve_nnls(A, b):
    """Solve using the non-negative least-square solution"""
    return optimize.nnls(A, b)[0] # sol, rest = nnls(A, b)

def solve_linprog(c, A, b, t):
    """Solve using the Scipy.optimize.linprog's simplex algorithm"""
    result = optimize.linprog(c, None, None, A, b)
    if result.status == 0 and result.x[t]>0: #result is optimal and not bounded
        return result
    elif result.status == 3 : #unbounded    
        return result
        pass
    else : #Infeasable?
        return None
    
    
#cut is a lambda fonction of the condition to test. its input will be the solution vector at each iteration of phase 2
def solve_linprog_with_callback(c, A, b, cut):
    """Solve using the Scipy.optimize.linprog's simplex algorithm and cuting second-step with callback function"""
    #Callback function, will be use to stop the simplex when it has a valid solution respecting strict constraint
    def cut_callback(xk, **kwargs) :
        print("strictpositive fct : xk = ",xk, xk[t]>0)
        print(kwargs)
        if kwargs["phase"] == 2 and cut(xk) :
            print("Found solution and aborted the rest of the simplex :",xk)
            raise FoundSolution(xk)

    try :
        #http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
        #solve (exist v | v>=0 and C_{PxT1}v = m - m0)                                               
        result = optimize.linprog(c, None, None, A, b, callback = strict_positive_t)
        
    except FoundSolution as f :
        return f.solution
    return None             


def solve_sympy(c, A, b):
    """Solve using symbolic calculation from SymPy"""
    pass

#e est l'indice de la contrainte strictement positive
def solve_qsopt(c, A, b, e):
    r = solve_with_qsopt(c, A, b)    

    if r.status == qsoptex.SolutionStatus.INFEASIBLE :
        print("QSOPT : INFEASABLE")
        return None
                
    elif r.status == qsoptex.SolutionStatus.UNBOUNDED :
        print("Unbounded")
        d = [0 for x in c]
        
        A_up = np.array([[one_if_equal(i,e) for i, x in enumerate(c)]])
        b_up = [1]
        r = solve_with_qsopt(d, A, b, A_up, b_up)
        
        if r.status == qsoptex.SolutionStatus.INFEASIBLE :
            A_up = np.array([[objective(i,e) for i,x in enumerate(c)]])
            b_up = [-1]
            r = solve_with_qsopt(d, A, b, A_up, b_up, qsoptex.ObjectiveSense.MAXIMIZE)
            
    assert r.status == qsoptex.SolutionStatus.OPTIMAL
    print("QSOPT_EX return ",type(r.x[0]),r.x)
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
            d = {} # dictionnary representing the constraint
            for x in range(0, n):
                d[x] = int(line.flatten()[x])

            p.add_linear_constraint(qsoptex.ConstraintSense.GREATER, d, int(b_up[index]))


                    
    p.set_objective_sense(objective)
    p.set_param(qsoptex.Parameter.SIMPLEX_DISPLAY, 0)
    p.set_param(qsoptex.Parameter.SIMPLEX_MAX_ITERATIONS,1)

    result = Bunch(status=p.solve(),x=[])

    if result.status == qsoptex.SolutionStatus.OPTIMAL :
        # récupération de la valeur de la solution
        for j in range(0, n):
            result.x.append(p.get_value(names[j]))
        print("solution", *result.x)

        return result
        
    return result

