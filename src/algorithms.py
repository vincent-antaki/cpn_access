#!/usr/bin/python
# -*- coding: utf-8 -*-
from petrinet import *
import numpy as np
from fractions import Fraction

verbose = False

"""
Fireable and Reachable algorithms from : 

[FH13] - Fraca and Haddad, Complexity Analysis of Continous Petri Net. 2013.

"""
def fireable(net, m, t1):
    """
    Fireable algorithm from [FH13] - Section 3

    Input : 
        net : a continous petri net system, represented by a numpy reccord array with 2d tuples as elements
        m : an initial marking, represented by a 1-dimension numpy array
        t1 : an numpy array of ordered indexes reprensenting a subset of the net's transitions

    Output : (fireable?, t2)
        fireable? : a boolean that indicates if all t1 can be fired
        t2 : returns the maximal firing set include in t1 (if fireable == true => t1 == t2)
                
    """
    assert net.shape[0] == m.shape[0]
    t2,p = np.empty((0,),dtype=np.int), m.nonzero()[0]
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
    
def reachable(net, m0, m, limreach=False, solver='qsopt-ex'):
    """
    Reachable algorithm from [FH13] - Section 4

    Input : 
        net : a continous petri net system, represented by a numpy reccord array with 2d tuples as elements
        m0 : an initial marking, represented by a 1-dimension numpy array
        m : a final marking, represented by a 1-dimension numpy array
        limreach : if true, reachable will test the lim-reachability of marking m
        solver : the solver to use
        
    Output : 
        sol : False if not reachable, else returns Parikh Image of solution, represented by a 1d numpy array.
        
    """
    
    n1, n2 = net.shape
    assert len(m) == n1 and n1 == len(m0)
    
    #initialy, t1 represents all the transitions of the Petri net system
    t1 = np.arange(n2,dtype=np.int)

    if np.array_equiv(m,m0) : 
        return [0 for x in t1] 
        
    b_eq = np.array(m - m0)
    
    while t1.size != 0:
        l = t1.size
        nbsol, sol = 0,np.zeros(l,dtype=Fraction)  
        A_eq = incident(subnet(net,t1))

        for t in range(0,l):
            result=None
                            
            if solver=='qsopt-ex':    
                result = solve_qsopt(A_eq, b_eq, t)
            elif solver=='GLPK':
                result=solve_GLPK(A_eq, b_eq, t)
            elif solver=='z3':
                result=solve_z3(A_eq, b_eq, t)
            elif solver=='scipy':
                try :
                    result=solve_scipy(A_eq, b_eq, t)    
                except FoundSolution as f :
                    pass
            else :
                raise Exception("No valid solver given")
                    
            if result.status == 'feasible' :
                nbsol += 1
                sol += result.x
            elif verbose and result.status != 'infeasible' :
                print(solver+' finished with status '+result.status+' on the following problem :')
                print("A_eq :", A_eq)            
                print("b_eq :", b_eq)
                print("Strict positive constraint on transition ", t)
        
        if nbsol == 0 :
            #No solution, there is no combination of the transitions that can be equal to m-m0.
            if verbose : print("No solution")
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

def coverability(net, m0, m, limreach=False, solver='qsopt-ex'):
    """
    Coverability algorithm from [FH15]

    Input : 
        net : a continous petri net system, represented by a numpy reccord array with 2d tuples as elements
        m0 : an initial marking, represented by a 1-dimension numpy array
        m : a final marking, represented by a 1-dimension numpy array
        limreach : if true, reachable will test the lim-reachability of marking m
        solver : the solver to use

    Output : 
        sol : False if not reachable, else returns Parikh Image of solution, represented by a 1d numpy array.
        
    """
    n1, n2 = net.shape
    assert len(m) == n1 and n1 == len(m0)
    
    #initialy, t1 represents all the transitions of the Petri net system
    t1 = np.arange(n2,dtype=np.int)

    if np.array_equiv(m,m0) : 
        return [0 for x in t1] 
        
    b_eq = np.array(m - m0)
    
    while t1.size != 0:
        l = t1.size
        nbsol, solv, solw = 0,np.zeros(l,dtype=Fraction), np.zeros(l,dtype=Fraction)  
        A_eq = incident(subnet(net,t1))

        for t in t1:
            result=None
                            
                    
            if result.status == 'feasible' :
                nbsol += 1
                solv += result.v
                solw += result.w
                
            elif verbose and result.status != 'infeasible' :
                print(solver+' finished with status '+result.status+' on the following problem :')
                print("A_eq :", A_eq)            
                print("b_eq :", b_eq)
                print("Strict positive constraint on transition ", t)
        
        if nbsol == 0 :
            #No solution, there is no combination of the transitions that can be equal to m-m0.
            if verbose : print("No solution")
            return False 

        else :
            y = Fraction(1,nbsol)
            solv = [x * y for x in list(solv)]
            solv = np.array(solv,dtype=Fraction) 
            solw = [x * y for x in list(solw)]
            solw = np.array(solw,dtype=Fraction) 


        t1 = solv.nonzero()[0]
        sub, subplaces = subnet(net, t1, True) 
        t1 = np.intersect1d(t1, maxFS(sub, m0.take(subplaces)),assume_unique=True)
        
        if not limreach :
            t1 = np.intersect1d(t1, maxFS(reversed_net(sub), (m+solw).take(subplaces)),assume_unique=True)


        if np.array_equiv(t1,sol.nonzero()) :
            #Found a solution. yay.
            return sol

    return False


class FoundSolution(Exception):
    def __init__(self, solution):
        self.solution = solution

def if_equal(a, b, true_value, default_value):
    if a == b : return true_value
    else : return default_value

#e is the index of the strict probability constraint.
def solve_qsopt(A, b, e):
    import qsoptex
    global qwe
    c = [-1 if x==e else 0 for x in range(0,A.shape[1])]    
    r = solve_with_qsopt(c, A, b)    

    if r.status == qsoptex.SolutionStatus.INFEASIBLE or (r.status == qsoptex.SolutionStatus.OPTIMAL and r.x[e] == 0):
        #QSopt_ex : INfeasible
        return Bunch(status='infeasible',x=None)
                
    elif r.status == qsoptex.SolutionStatus.UNBOUNDED :
        #QSopt_ex : UNBOUNDED
        d = [0 for x in c]
        
        A_up = np.array([[if_equal(i,e,1,0) for i, x in enumerate(c)]])
        b_up = [1] #this is an arbitrairy cut
        r = solve_with_qsopt(d, A, b, A_up, b_up)

    if r.status == qsoptex.SolutionStatus.OPTIMAL :
        r.status = 'feasible'
    elif r.status == qsoptex.SolutionStatus.ITER_LIMIT:
        r.status = 'iter_limit_reached'
                           
    elif r.status == qsoptex.SolutionStatus.TIME_LIMIT:
        r.status = 'time_limit_reached'                   

    return r
    
    
def solve_with_qsopt(c, A_eq, b_eq, A_up=None, b_up=None, objective=None):
    """Solve using QSopt_ex"""
    assert A_eq.shape[0] == len(b_eq)
    import qsoptex      
    
    if objective==None:
        objective = qsoptex.ObjectiveSense.MINIMIZE
    
    
    p = qsoptex.ExactProblem()
    names = []
    n = len(c)
    
    for i, x in enumerate(c):
        names.append(bytes([i]))
        p.add_variable(name=names[i],objective=x,lower=0)

    Atype = type(A_eq) 
    if Atype == np.matrix :
        for index, line in enumerate(A_eq) :
            d = {} # dictionnary representing the equality constraints
            for x in range(0, n):
                d[x] = int(line.getA1()[x])
            p.add_linear_constraint(qsoptex.ConstraintSense.EQUAL, d, int(b_eq[index]))

    elif Atype == np.recarray or Atype == np.ndarray or Atype == np.array :
        for index, line in enumerate(A_eq) :
            d = {} # dictionnary representing the equality constraints
            for x in range(0, n):
                d[x] = int(line[x])

            p.add_linear_constraint(qsoptex.ConstraintSense.EQUAL, d, int(b_eq[index]))
        
    else :
        raise TypeError("A_eq type is not recognize.")            
        
    if A_up is not None and b_up is not None :
        assert A_up.shape[0] == len(b_up)
        for index, line in enumerate(A_up) :
            d = {} # dictionnary representing the inequality constraints
            flat = line.flatten()
            for x in range(0, n):
                d[x] = int(flat[x])

            p.add_linear_constraint(qsoptex.ConstraintSense.GREATER, d, int(b_up[index]))
        
    p.set_objective_sense(objective)
    p.set_param(qsoptex.Parameter.SIMPLEX_DISPLAY, 0)
    result = Bunch(status=p.solve(),x=[])

    if result.status == qsoptex.SolutionStatus.OPTIMAL :
        # récupération de la valeur de la solution
        for j in range(0, n):
            result.x.append(p.get_value(names[j]))
        
    return result

def solve_GLPK(o, A_eq, b_eq, t) :
    pass
    
def solve_z3(A_eq, b_eq, t):
    """Solve using Microsoft z3"""
    import z3
    s = z3.Solver()
    x = [z3.Real("x_%i" % (i+1)) for i in range(0,A_eq.shape[1])]

    for j in range(0,A_eq.shape[1]):
        if j == t :
            s.add(0 < x[j])        
        else :
            s.add(0 <= x[j])
            
    Atype = type(A_eq) 
    if Atype == np.matrix :
        for i in range(0,A_eq.shape[0]) :
            s.add(z3.Sum([A_eq[i].getA1()[j]*x[j] for j in range(0,A_eq.shape[1])]) == b_eq[i])

    else :
        for i in range(0,A_eq.shape[0]) :
            s.add(z3.Sum([A_eq[i][j]*x[j] for j in range(0,A_eq.shape[1])]) == b_eq[i])
    
    if s.check() == z3.sat:
        if verbose : print("Solution found")
        m = s.model()
        r = np.array([Fraction(m[x[j]].numerator_as_long(),m[x[j]].denominator_as_long()) for j in range(0,A_eq.shape[1])], dtype=Fraction)
        return Bunch(x=r,status='feasible')

    else :
        if verbose : print("No solution found")
        return Bunch(status='infeasible')

def solve_linprog(A_eq, b_eq, t):
    """Solve using the Scipy.optimize.linprog's simplex algorithm"""
    result = optimize.linprog(c, None, None, A, b)
    if result.status == 0 and result.x[t]>0: #result is optimal and not bounded
        return result
    elif result.status == 3 : #unbounded    
        return result
        pass
    else : #Infeasible?
        return None
    
## You need to upgrade to scipy >=0.16.0 for it to work    
def solve_scipy(A_eq, b_eq, t):
    """Solve using the Scipy.optimize.linprog's simplex algorithm and cuting second-step with callback function"""
    import scipy.optimize as opt
    #Callback function, will be use to stop the simplex when it has a valid solution respecting strict constraint
    def cut_callback(xk, **kwargs) :
        print("strictpositive fct : xk = ",xk, xk[t]>0)
        print(kwargs)
        if kwargs["phase"] == 2 and xk[t]>0 :
#            x = calculate_vector_from_basis()
            
            print("Found solution and aborted the rest of the simplex :",xk)
            raise FoundSolution(xk)

    try :
        #http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
        #solve (exist v | v>=0 and C_{PxT1}v = m -m0)                                               
        result = opt.linprog([if_equal(t,x,1,0) for x in range(0,A_eq.shape[1])], None, None, A_eq, b_eq, callback = cut_callback)        
    except FoundSolution as f :
        #x = confirme here that the result is valid 
        return Bunch(status='feasible',x=f.solution)
        
    #assert with Farkas here    
    return Bunch(status='infeasible',x=None) 


def solve_stp(A_eq, b_eq, t):    
    pass
    
class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def __str__(self):
        return str(self.__dict__)
