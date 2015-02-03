import numpy as np

def incident(net):
    return np.matrix(net['post'], dtype='int64') - np.matrix(net['pre'], dtype='int64')

#v is the an orderedlist of index of a transitions or a places
#if place is True, fonction returns an ordered list of indexes v's input transitions (nonzero output transitions) indexes
#else : input is a transition index, fct returns v's input places (nonzero i) 
#
def preset(net, v, place=False):
    if place:
        return np.unique(net['post'][v].nonzero()[1].getA1())
    else :
        return np.unique(net['pre'].take(v,axis=1).nonzero()[0].getA1())

def postset(net, v, place=False) :
    if place:
        return np.unique(net['pre'][v].nonzero()[1].getA1())
    else :
        return np.unique(net['post'].take(v,axis=1).nonzero()[0].getA1())

def reversed_net(net):
    dtype = net.dtype
    dtype.names = ['post', 'pre']
    return np.matrix(net, dtype=dtype)

#soit t, un array qui contient les index des transitions

# t : an array of index of the transitions to transfer to subnet
#subnet : a PetriNet instance with only the transitions in t and (if subplaces == True)

#return : if subplaces == False : return subnet
#         if subplaces : return (subnet,subplaces)

def subnet(net, t, subplaces = False):

    assert (all(x >= 0) and all(x < net['post'].shape[1]) for x in t)

    #one-liner moins lourd, a tester
    print(net)
    print("t",t)
    if subplaces == True:
        print(preset(net,t[0]),postset(net,t[0]))
        presub = [np.concatenate(preset(net,x),postset(net,x)) for x in t]
        print("presub", presub)
        subplaces = np.unique(presub).sort()

        #subplaces = list(set(np.concatenate([preset(net, x) for x in t])).union(set(np.concatenate([postset(net, x) for x in t]))))
        print(subplaces)
        return net.take(t, axis=0).take(subplaces, axis=1), subplaces
    else :
        return net.take(t, axis=1)

petrinet = np.matrix([
        [(2, 0), (0, 0), (3, 8), (1, 2), (0,37)],
         [(0, 3), (1, 3), (5, 0), (5, 2), (23,0)]],
         dtype=[('pre', 'uint'), ('post', 'uint')])

#print("net:", petrinet)
#print("preset:", preset(petrinet, [2]))
#print("postset:", postset(petrinet, [1]))
#print("reversed", reversed_net(petrinet))
#print("subnet:", subnet(petrinet, [1, 3]))
