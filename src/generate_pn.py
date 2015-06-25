#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import petrinet as pn
from scipy import stats
from random import *
import sys
import pickle

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
    distribution = [np.arange(maximum+1),[p if i==0 else (1-p)/maximum for i in range(0,maximum+1)]]
    random_var = stats.rv_discrete(values=distribution)

    nb_t = net.shape[1]
    r = random_var.rvs(size=nb_t)
    c = pn.incident(net)
    m = np.dot(c,r) + m0
    print(m)

    return m

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
                
                
                
