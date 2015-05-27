#!/usr/bin/python
# -*- coding: utf-8 -*-
import itertools
import numpy as np
from copy import deepcopy
"""
In this document, Petri nets are represented by instances of numpy.ndarray

for general documentation on numpy.recarray

http://docs.scipy.org/doc/numpy/reference/generated/numpy.recarray.html
http://docs.scipy.org/doc/numpy/reference/generated/numpy.core.records.fromrecords.html
>>> import numpy as np
>>> petrinet = np.matrix([[(2, 0), (0, 0), (3, 8), (1, 2), (0,37)],
                      [(0, 3), (1, 3), (5, 0), (5, 2), (23,0)]],
                      dtype=[('pre', 'uint'), ('post', 'uint')]) 

Generally, Petri Nets are represented by a matrix PRE and a matrix POST. 
We use a matrix with 2-dimensions tuples as elements.
(pre_ij,post_ij) for i in rows for j in columns

pre_ij : the number of token needed from place i to activate transition j
post_ij : the number of token given to place i when transition j is activated.

Basic manipulations tutorial! 

>>> petrinet['pre']
matrix([[ 2,  0,  3,  1,  0],
        [ 0,  1,  5,  5, 23]], dtype=uint64)
>>> petrinet['post']
matrix([[ 0,  0,  8,  2, 37],
        [ 3,  3,  0,  2,  0]], dtype=uint64)
        
>>> np.take(petrinet, [0], axis=None)
matrix([[(2, 0)]], 
       dtype=[('pre', '<u8'), ('post', '<u8')])

>>> np.take(petrinet, [0], axis=0)
>>> petrinet[0]     #same
matrix([[(2, 0), (0, 0), (3, 8), (1, 2), (0, 37)]], 
       dtype=[('pre', '<u8'), ('post', '<u8')])
       
>>> np.take(petrinet, [2], axis=1) 
>>> petrinet[:,2] #donne meme chose que la ligne précédente
matrix([[(3, 8)],
        [(5, 0)]], 
       dtype=[('pre', '<u8'), ('post', '<u8')])
              

"""
def incident(net):
    return np.matrix(net['post'], dtype='int64') - np.matrix(net['pre'], dtype='int64')

def preset(net, v, place=False):
    """
    v is an ordered list of index of transitions or places
    if place is True : input is a place index 
                       fonction returns an ordered list of v's input transitions indexes
    else : input is a transition index, 
           fonction returns an ordered list of v's input places indexes
    """
    a = None
    if place:
        a = net['post'][v].nonzero()[1]
    else :
        a = net['pre'].take(v,axis=1).nonzero()[0]    

    if type(a) == np.matrix :
        return np.unique(a.getA1())
    else : #type(a) == np.array or type(a)== np.rec.array 
        return np.unique(a)

def postset(net, v, place=False) :
    """
    v is an index of transition or place
    if place is True : input is a place index 
                       fonction returns an ordered list of v's output transitions indexes
    else : input is a transition index, 
           fonction returns an ordered list of v's output places indexes
    """
    a = None
    if place:
        a = net['pre'][v].nonzero()[1]
    else :
        a = net['post'].take(v,axis=1).nonzero()[0]

    if type(a) == np.matrix :
        return np.unique(a.getA1())
    else : #type(a) == np.array or type(a)== np.rec.array 
        return np.unique(a)

 
def reversed_net(net):
    """
    return a copy of the net but with the 'pre' and the 'post' label are inversed. Which conceptually gives a cpn with opposition flow. 
        i.e. net.dtype = ['pre':'uint','post':'uint']
             rev.dtype = ['post':'uint','pre':'uint']
    """
    dtype = deepcopy(net.dtype)
    dtype.names = net.dtype.names[::-1]
    rev = np.matrix(net, copy=True)
    rev.dtype = dtype
    return rev
    
def subnet(net, t, subplaces = False):
    """
    This function returns a copy of the cpn-system net but with only a subset of its transitions and, if subplaces == true, a subset of its places.

    Inputs :    
        net : a CPN system, represented by a numpy.matrix
        t : an ordered list of index of the variable net
        subplaces : if true, the returned net will only have the places that are in the preset or postset of a transition in t.
                    else, will keep all places.
                    
    Output : The format of the output changes according to the value of the boolean subplaces.
        if subplaces == False : return subnet
        if subplaces == True : return (subnet,subplaces)
        subnet : a CPN system that has a subset of with only the transitions in t and (if subplaces == True)
        subplaces : the indexes of the kept places

    """
    assert (all(x >= 0) and all(x < net['post'].shape[1]) for x in t)
        
    if subplaces == True:
        subplaces = np.union1d(preset(net,t),postset(net,t))
        #subplaces = list(set(np.concatenate([preset(net, x) for x in t])).union(set(np.concatenate([postset(net, x) for x in t]))))
        return net.take(t, axis=1).take(subplaces, axis=0), subplaces
    else :
        return net.take(t, axis=1)
