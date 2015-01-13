import numpy as np

class PetriNet:

    #takes regular python arrays in input, has numpy matrix as attributes.
    def __init__(self, pre, post):
    
        self.pre = np.matrix(pre) #size of both matrix P x T, every elements of those matrix are non-negative
        self.post = np.matrix(post)
        assert self.pre.shape == self.post.shape
    
    def incidenceMatrix(self):
        return self.post - self.pre       
    
    #v is the index of a transition or a place    
    #if place is True, it return v's input transitions that leads to v
    #else : input is a transition index, fct returns v's input places
    #
    def preset(self, v, place=False):
        if place:
            return self.post[v].nonzero()
        else
            return self.pre.transpose()[v].nonzero()

    #vieille version, faire comme preset    
    def postset(self, v, place=False):
        if v in self.places:
            return set([t for t in self.trans if not self.pre[v,t] == 0])
        elif v in self.trans
            return set([p for p in self.places if not self.post[p,v] == 0])
        else raise Exception("argument not in places or transitions of net")
    
    def reverseNet(self):
        return PetriNet(self.post, self.pre)

    #soit t, qui contient les index des transitions            
    def subnet(self, t):
        [assert x <= self.post.shape[1] for x in t]
        subplaces = set([preset(x) for x in t]).union(set([postset(x) for x in t]))
        
        
        take(self.pre.take(t,axis=1),...subplaces...) # dats the fonction to use. 
        take(self.post.take(t,axis=1),...subplaces...)
        
        return PetriNet(subplaces, t, ) #.......finish me plz.

    def __str__(self) :
        return "{ pre: "+str(self.pre)+" ,pos :"+ str(self.post)+ " }"

def petrinet_test():
    pre = [[1, 0, 0, 0], [1, 2, 0, 1], [0, 0, 1, 0]]
    post = [[0, 3, 1, 0], [1, 0, 0, 0], [2, 1, 0, 1]]
    p = PetriNet(pre, post)
    
