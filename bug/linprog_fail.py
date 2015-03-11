import numpy as np
from scipy import optimize  
 
x = np.matrix([[(1,0), (1,3), (0,1), (1,0)],
                [(1,1), (2,0), (0,0), (0,0)],
                [(0,0), (0,1), (1,0), (0,1)]],
        dtype=[('pre', 'uint'), ('post', 'uint')])
a  = np.matrix([[1,-2,-1,1],
                [0,2,0,0],
                [0,-1,1,-1]],
        dtype='int64')      
c = np.array([1,-2,0])
b = np.array(
       [[-1, 1],
        [1, -1]],
dtype='int64')
m = np.array([-2,2])
t=0
def objective(t,x):
    if t == x : return -1
    else : return 0

objective_vector = np.array([objective(t,x) for x in range(0,b.shape[1])])


class FoundSolution(Exception):
    def __init__(self, solution):
        self.solution = solution 
def strict_positive_t(xk, **kwargs) :
    print("strictpositive fct : xk = ",xk, xk[t]>0)
    print(kwargs)
    
    if kwargs["phase"] == 2 and xk[t] > 0 :
        print("Found solution :",xk)
        raise FoundSolution(xk)        


print(objective_vector)
print(None)
print(b)
print(None) 
print(m) 
try :
    if True :
        #celui qui marche
        result = optimize.linprog(objective_vector,A_eq=b, b_eq=m)
    
    else :    
        #celui qui crash de manière étrange
        #result = optimize.linprog(objective_vector, A_eq=b, b_eq=m, callback = strict_positive_t)
                result = optimize.linprog(np.array(objective_vector), A_eq=b, b_eq=m, callback = lambda *x, **kwargs: None)
except FoundSolution as f:
    print("Solution :",f)
print("Resultat :", result.x)    
print(result)
