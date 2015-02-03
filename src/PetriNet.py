import numpy as np
from contracts import pre, post

class PetriNet:

    #takes regular python arrays in input, has numpy matrix as attributes.
    def __init__(self, pre, post):

        self.pre = np.mat(pre) #size of both matrix P x T, every elements of those matrix are non-negative
        self.post = np.mat(post)
        assert self.pre.shape == self.post.shape
        self.shape = self.pre.shape


    def incidenceMatrix(self):
        return self.post - self.pre

    #v is the index of a transition or a place
    #if place is True, it return v's input transitions that leads to v
    #else : input is a transition index, fct returns v's input places
    #
    def preset(self, v, place=False):
        if place:
            return self.post[v].nonzero()[1].getA1()
        else :
            return self.pre.take(v,axis=1).nonzero()[1].getA1()

    def postset(self, v, place=False) :
        if place:
            return self.pre[v].nonzero()[1].getA1()
        else :
            return self.post.take(v,axis=1).nonzero()[1].getA1()

    def reverseNet(self):
        return PetriNet(self.post, self.pre)

    #soit t, un array qui contient les index des transitions

    # t : an array of index of the transitions to transfer to subnet
    #subnet : a PetriNet instance with only the transitions in t and (if subplaces == True)

    #return : if subplaces == False : return subnet
    #         if subplaces : return (subnet,subplaces)

    def subnet(self, t, subplaces = False):

        assert (all(x >= 0) and all(x < self.post.shape[1]) for x in t)

        #subplaces = np.unique([np.concatenate((self.preset(x),self.postset(x))) for x in t]).sort()
        #one-liner moins lourd, a tester
        if subplaces :
            subplaces = list(set(np.concatenate([self.preset(x) for x in t])).union(set(np.concatenate([self.postset(x) for x in t]))))
            return (PetriNet(np.take(self.pre.take(t,axis=1),subplaces,axis=0),np.take(self.post.take(t,axis=1),subplaces,axis=0)), subplaces )
        else :
            return PetriNet(self.pre.take(t,axis=1),self.post.take(t,axis=1))



    def __str__(self) :
        return "{ pre: \n"+str(self.pre)+",\npos :\n"+ str(self.post)+ " }"

def getTestPetriNet():
    pre = ((1, 1, 0, 1),
            (1, 2, 0, 0),
            (0, 0, 1, 0))

    post = ((0, 3, 1, 0),
            (1, 0, 0, 0),
            (0, 1, 0, 1))
    return PetriNet(pre, post)

def apply_transition(net, m0, transitions):
    for t in transitions:
        m0 -= net.pre.transpose()[t]
        assert m0[m0 < 0].size == 0
        m0 += net.post.transpose()[t]
        yield m0.copy()

if __name__ == '__main__':
    net = getTestPetriNet()
    z=apply_transition(net, (2, 7, 3), [1, 0, 2, 3, 2, 0])
    print(list(z))







