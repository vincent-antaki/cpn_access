import numpy as np

from petrinet import preset, postset

#takes in input :
#n, a petriNet instance;
#m, a numpy array representing an initial marking;
#t1, an array of ordered index representing a subset of transitions of n
#
def fireable(net, m, t1):
    t2,p = np.empty(1), m.nonzero()[0]
    t1 = np.array(t1)
    assert n.shape[0] == m.shape[0]

    while np.setdiff1d(t1,t2).size != 0:
        new = False
        for t in np.setdiff1d(t1,t2) :
            if all(np.in1d(n.preset(t),p,assume_unique=True)) :
                t2, p, new = np.union1d(t2,[t]), np.union1d(p, postset(net, t)), True
        if not new : return (False, t2)
    return (True,None)