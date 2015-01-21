import numpy as np

def incident(net):
    return net['post'] - net['pre']

#v is the index of a transition or a place
#if place is True, it return v's input transitions that leads to v
#else : input is a transition index, fct returns v's input places
#
def preset(net, v, place=False):
    if place:
        return net['post'][v].nonzero()[1].getA1()
    else :
        return net['pre'].take(v,axis=1).nonzero()[1].getA1()

def postset(net, v, place=False) :
    if place:
        return net['pre'][v].nonzero()[1].getA1()
    else :
        return net['post'].take(v,axis=1).nonzero()[1].getA1()

def reversed_net(net):
    return np.matrix(net, dtype=[('post', 'uint'), ('pre', 'uint')])

#soit t, un array qui contient les index des transitions

# t : an array of index of the transitions to transfer to subnet
#subnet : a PetriNet instance with only the transitions in t and (if subplaces == True)

#return : if subplaces == False : return subnet
#         if subplaces : return (subnet,subplaces)

def subnet(net, t, subplaces = False):

    assert all(x >= 0 and x < net['post'].shape[1] for x in t)

    #subplaces = np.unique([np.concatenate((net['pre']set(x),net['post']set(x))) for x in t]).sort()
    #one-liner moins lourd, a tester
    if subplaces == True:
        subplaces = list(set(np.concatenate([preset(net, x) for x in t])).union(set(np.concatenate([postset(net, x) for x in t]))))
        return net.take(t, axis=0).take(axis=1)
    else :
        return net.take(t, axis=1)

# example de réseau de petri
petrinet = np.matrix([
        [(1, 2), (5, 6), (7, 8), (9, 0)],
        [(1, 2), (5, 6), (7, 8), (9, 0)]],
        dtype=[('pre', 'uint'), ('post', 'uint')])

print("net:", petrinet)
print("preset:", preset(petrinet, [2]))
print("postset:", postset(petrinet, [1]))
print("reversed", reversed_net(petrinet))
print("subnet:", subnet(petrinet, [1, 3]))
