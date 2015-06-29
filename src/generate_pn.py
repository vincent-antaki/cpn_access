#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from scipy.signal.windows import general_gaussian
import petrinet as pn
from scipy import stats,optimize
from random import *
import sys
import pickle
from fractions import Fraction

maximum=10
quantity_to_build = {'verysmall':10,
'small':10,
'medium':5,
'big':1,
'huge':1,
'gigantic':1}
sizedef={'verysmall':range(2,6),
'small':range(5,15),
'medium':range(15,35),
'big':range(35,65),
'huge':range(65,150),
'gigantic':range(150,300)}

"""
size : le type de taille que l'on désire
qte : la quantité à générer
p : la probabilité que Pre ou Post soit dégénéré.
no_degenerate_transition_or_counter : aucune transition vide ou de compteurs isolé

return a list of tuples (net, m0, m) where net is a the generated net, m0 and m are markings (in integer).

"""
def generate_pn_by_size(size='small',qte=10, p=0.55, c_leq_t=False,no_degenerate_transition_or_counter = True):    
    
    pns = []
    distribution = [np.arange(maximum+1),[p if i==0 else (1-p)/maximum for i in range(0,maximum+1)]]
    random_var = stats.rv_discrete(values=distribution) 

    while qte > 0 :
        c = choice(sizedef[size])
        t = choice(sizedef[size])    

        if not c_leq_t or c <= t :
            net = generate_pn((c,t),random_var)
            m0,m = None,None
            if no_degenerate_transition_or_counter :
                while not assert_ok(net):
                    net = generate_pn((c,t),random_var)
                    
            m0,m = getM(c),getM(c)                               
            pns.append((net,m0,m))             
            #pns.append(m0)             
            #pns.append(m)            
            
        qte -= 1    

    return pns            


"""
Generate a marking of length c where each element are [0,maximum].
"""
def getM(c):
    return np.array([randint(0,maximum*2) for i in range(0,c)])


"""
Generate a marking that match the net shape. The marking is a linear combination of the transitions of a net + m0
"""
def getM2(net, m0, p):
    done = False
    while(not done):
        distribution = [np.arange(3+1),[p if i==0 else (1-p)/3 for i in range(0,4)]]
        random_var = stats.rv_discrete(values=distribution)

    ## A Retirer
    #    nb_t = net.shape[1]
    #    c = pn.incident(net)
    #    ok = False
    #    while(!ok):
    #        r = np.array(random_var.rvs(size=nb_t))
    #        b_up = np.append(m0,r)
    #        a_up = np.vstack((-1*c,(-1 * np.eye((nb_t,nb_t)))
     #
     #      result = optimize.linprog(A_up = a_up,b_up = r)
      #      print(result.status)
      #      assert()
     #       print(result.x)
    #        m = np.dot(c,r) + m0
    #
    #        if all([i >= 0 for i in m]):
    #            ok = True
    #        print(m)
    #
    ##
        nb_t = net.shape[1]
        import z3
        s = z3.Solver()
        c = np.array(pn.incident(net))
        r = np.array(random_var.rvs(size=nb_t))
        b_up = np.append(-1*m0,r)

        e = np.eye(nb_t,dtype=np.int)
        a_up = np.vstack((c, e))#

        print(e,e.dtype)
        print(c,c.dtype)


        v = [z3.Int("x_%i" % (i+1)) for i in range(0,a_up.shape[1])]
        #v = z3.IntVector('v',a_up.shape[0])
        print("c : ", c, ", r : ",r)
        print("A_up shape : ",a_up.shape,"b_up shape : ", b_up.shape)

        assert a_up.shape[0] == b_up.size
        for i in range(0,b_up.size):
            s.add(z3.Sum([a_up[i][x]*v[x] for x in range(nb_t)]) >= b_up[i])


        if s.check() == z3.sat:
    #        if verbose :
            done = True
    #        print("Solution found")
            m = s.model()
    #        print(m)
            r = np.array([m[j].as_long() for j in v], dtype=np.int)
            print(r)
            q = np.dot(c,r)
            print("M : ", q)
            return q
        else :
            pass    
#        if verbose :
   #         print("No solution found")

def generate_pn(shape,random_var):
    """
    shape : a pair of int>0 specifying the number of counters and the number of transitions. 
    p : La probabilité qu'il y aille un arc
    maximum : le nombre maximal qu'il peut y avoir dans une matrice Pre et Post.

    Si (i,j) n'est pas 0, choisie de avec probabilité égale un nombre entre 1 et maximum.
    """
    u = list(zip(random_var.rvs(size=shape[0]*shape[1]),random_var.rvs(size=shape[0]*shape[1])))    
    return np.rec.array(u,shape=shape,dtype=[('pre', 'uint'), ('post', 'uint')])

"""
Corrects transitions so there are no isolated counters and there are no transition that only takes or only gives chips to the counters.
(see function assert_ok(net) )
"""
def correct_pn(net):
    for t in range(0,net.shape[1]):
        if not any([net['pre'][c][t] != 0 for c in range(0,net.shape[0])]):
            c = random.randInt(0, net.shape[0])
            while net['pre'][c][t] == 0 :
                net['pre'][c][t] = uniform_dist.rvs(size=1)
        if not any([net['post'][c][t] != 0 for c in range(0,net.shape[0])]):
            c = random.randInt(0, net.shape[0])
            while net['post'][c][t] == 0 :
                net['post'][c][t] = uniform_dist.rvs(size=1)

    for c in range(0,net.shape[0]):
        if all([net['pre'][c][t] ==0 and net['post'][c][t] ==0 for t in range(0,net.shape[1])]):
            t = random.randInt(0,net.shape[1])
            pre = random.randInt(0,1)
            if pre :
                while net['pre'][c][t] == 0 :
                    net['pre'][c][t] = uniform_dist.rvs(size=1)


"""
Verify that each transition of the Petri net has at least one non-zero element in the pre matrix and one non-zero element in the post matrix.

Verify that there are no isolated counters.

"""
def assert_ok(net):
    #parcourir le net pour voir qu'il n'y a pas de transition abberantes
    for t in range(0,net.shape[1]):

        if all([net['pre'][c][t] == 0 for c in range(0,net.shape[0])]) or all([net['post'][c][t] == 0 for c in range(0,net.shape[0])]):
            return False
            
    for c in range(0,net.shape[0]):
        if all([net['pre'][c][t] == 0 and net['post'][c][t] == 0 for t in range(0,net.shape[1])]):
            return False
                    
    return True    
  
"""
save an array of np arrays
"""  
def _save(name, arrays):    
    #np.savez(name, *arrays)
    pickle.dump(arrays, open(name+'.p',"wb"))

def _load(name):
    return pickle.load(open(name+'.p',"rb"))
#    return np.load(name+'.npz')
        
"""
Makes a list of elements 
"""        
def load_n_tupleize(name):
    a = np.load(name+'.npz')
    print(a)
    b = [i[1] for i in a.iteritems()]
#    print(b)
    assert len(b) % 3 == 0
    pn_list = []
    for i in range(0,len(b)/3) :
        pn_list += ((b[i*3],b[i*3+1],b[i*3+2]))   
    #return pn_list
    return
problems = {}

if __name__ == '__main__':
    args = sys.argv
    
    if len(args) == 1 or len(args) == 2 :
        print("No argument given. use 'build *x' or 'read *x'")
        print("Where x in {all, verysmall, small, medium, huge, gigantic}")
    
    else :
        def readarguments():
            for arg in args[2:] :
                subjects = []            
                if arg == 'all':
                    return sizedef.keys() 
                    
                if arg in sizedef.keys():
                    subjects.append(arg)
                else :
                    print(arg+' is not a valid argument.')
                    sys.exit(0)
            return subjects

        if args[1] == "build" :
             
            for i in readarguments():
                a = generate_pn_by_size(size=i,qte = quantity_to_build[i])
                print(a)
                _save(i,a)
                
        elif args[1] == "read":
            
            readarguments()
            for i in readarguments():
                #print(load_n_tupleize(i))
                problems[i] = _load(i)
                print(problems[i])
        else :
            print(args[1]+' is not a valid command.')
            sys.exit(0)        
                
a = np.matrix(
               [[(1,0), (1,3), (0,1), (1,0)],
                [(1,1), (2,0), (0,0), (0,0)],
                [(0,0), (0,1), (1,0), (0,1)]],
        dtype=[('pre', 'uint'), ('post', 'uint')])

m0 = np.array([2,5,7])                
                
getM2(a,m0,0.2)
