from lxml import etree
import numpy as np
import sys

version = "{http://www.pnml.org/version-2009/grammar/pnml}"
#parser = etree.XMLParser(remove_blank_text=True)
class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def __str__(self):
        return str(self.__dict__)

class arc:
    def __init__(self, name, pnml_id, source, target, **kwds):
        self.name = name
        self.pnml_id = pnml_id
        self.source = source
        self.target = target
        self.__dict__.update(kwds)

class place:
    def __init__(self, name, pnml_id, initialmarking, **kwds):
        self.name = name
        self.pnml_id = pnml_id
        self.initialmarking = initialmarking
        self.__dict__.update(kwds)

class transitions:
    def __init__(self, name, pnml_id, **kwds):
        self.name = name
        self.pnml_id = pnml_id
        self.__dict__.update(kwds)

class PNML_and_numpy_net:
    def __init__(self, name, places, transitions, arcs):
        self.name = name
        self.places = places
        self.transitions = transitions
        self.generate_numpy_net()
    
    def generate_numpy_net(self) :
        pass
        
        
"""
Parse a .pnml file to a numpy representation.

"""        
def parse_pnml_tree(tree):
    root = tree.getroot()
    page = root.find(version+"net/"+version+"page")
    name = root.find(version+"net/"+version+"name/"+version+"text").text

    print(name)
    
    T = {}
    P = {}
    transitions = []
    places = []
    initial_marking = []        

    p_size = 0
    for p in page.iter(version+"place"):
        places.append(p)
        P[p.attrib['id']] = p_size
        #name = p.find(version+"name")
        initial_marking.append(int(p.find(version+"initialMarking/"+version+"text").text))
        p_size += 1
    
    t_size = 0    
    for t in page.iter(version+"transition"):
        transitions.append(t)
        T[t.attrib['id']] = t_size
        t_size += 1 
    
    pre = np.zeros(shape=(p_size,t_size))
    post = np.zeros(shape=(p_size,t_size))
    
    #net = np.core.recordarray([[(0,0) for j in range(0, t_size)]for i in range(0,p_size)], dtype=[('pre','uint'),('post','uint')])
    i =0
    print("patate")
    for a in page.iter(version+"arc"):
        print(i, " : ")
        source = a.attrib['source']
        target = a.attrib['target']
        #id = a.attrib['id']
        i+= 1
        if source in P.keys():
          #  net['pre'][P[source]][T[target]] = int(list(list(a)[0])[0].text) #paresseux
            pre[P[source]][T[target]] = int(list(list(a)[0])[0].text) #paresseux
        elif source in T.keys():
           # net['post'][P[target]][T[source]] = int(list(list(a)[0])[0].text)
            post[P[target]][T[source]] = int(list(list(a)[0])[0].text)
        else:
            raise Exception("The id of the arc's source is no where to be found.")

    net = np.rec.array(zip(pre.ravel(),post.ravel()), dtype=[('pre','uint'),('post','uint')]).reshape(pre.shape)

    nets.append(Bunch(p=P,t=T,tr=transitions,ini=initial_marking,pla=places))

    return net          

pnmls = []
nets = []

if __name__ == '__main__':
    args = sys.argv

    if len(args) == 1 :
        print("No file specified. Feed me some .pnml files!")
    else :
        #http://lxml.de/validation.html#relaxng
        pnmlmodel = etree.parse(open('pnmlcoremodel.rng', 'r'))
        grammar_validator = etree.RelaxNG(pnmlmodel)
    
        for arg in args[1:]:
            print("parsing something, or at least trying to.")
            pnml_file = open(arg,'r')
            pnmlnet = etree.parse(pnml_file)
            if grammar_validator(pnmlnet): #deconne. why???
                pnmls.append(pnmlnet)
                nets.append(parse_pnml_tree(pnml))        
            else :
                print("File "+arg+" could not be validated with PNML's core model grammar.")                  

