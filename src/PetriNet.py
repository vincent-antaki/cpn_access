import numpy as np

class PetriNet:

    #takes regular python arrays in input, has numpy matrix as attributes.
    def __init__(self, pre, post):
    
        self.pre = np.mat(pre) #size of both matrix P x T, every elements of those matrix are non-negative
        self.post = np.mat(post)
        assert self.pre.shape == self.post.shape
    
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
    def subnet(self, t):
        assert all(x >= 0 and x < self.post.shape[1] for x in t)
        subplaces = list(set(np.concatenate([self.preset(x) for x in t])).union(set(np.concatenate([self.postset(x) for x in t]))))  
        print(subplaces)
        return PetriNet(np.take(self.pre.take(t,axis=1),subplaces,axis=0),np.take(self.post.take(t,axis=1),subplaces,axis=0))

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

def petrinet_test():
    pre = ((1, 1, 0, 0), 
            (1, 2, 0, 1), 
            (0, 0, 1, 0))
            
    post = ((0, 3, 1, 0), 
            (1, 0, 0, 0), 
            (2, 1, 0, 1))
    p PetriNet(pre, post)    
    assert np.array_equal(p.preset(1),[0,1])
    assert np.array_equal(p.postset(1),[0,2])
    assert np.array_equal(p.preset(3),[1])
    assert p.preset(1, place=True) == [0]    
    assert np.array_equal(p.postset(0,True),[0,1]) 
    assert np.array_equal(p.postset(1,True),[0,1,3])
    assert np.array_equal(p.postset(1,True),[0,1,3])
