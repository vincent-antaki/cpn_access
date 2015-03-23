import itertools
import numpy as np
from copy import deepcopy
"""
In this document, Petri nets are reprensed by instances of numpy.matrix

for general documentation on numpy-matrix and numpy.recarray

http://docs.scipy.org/doc/numpy/reference/generated/numpy.recarray.html
http://docs.scipy.org/doc/numpy/reference/generated/numpy.core.records.fromrecords.html

petrinet = np.matrix([[(2, 0), (0, 0), (3, 8), (1, 2), (0,37)],
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
    v is an orderedlist of index of transitions or places
    if place is True : input is a place index 
                       fonction returns an ordered list of v's input transitions indexes
    else : input is a transition index, 
           fonction returns an ordered list of v's input places indexes
    """
    if place:
        return np.unique(net['post'][v].nonzero()[1].getA1())
    else :
        return np.unique(net['pre'].take(v,axis=1).nonzero()[0].getA1())

def postset(net, v, place=False) :
    """
    v is an index of transition or place
    if place is True : input is a place index 
                       fonction returns an ordered list of v's output transitions indexes
    else : input is a transition index, 
           fonction returns an ordered list of v's output places indexes
    """
    if place:
        return np.unique(net['pre'][v].nonzero()[1].getA1())
    else :
        return np.unique(net['post'].take(v,axis=1).nonzero()[0].getA1())
 
def reversed_net(net):
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
        t : a subset of index of the variable net
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
