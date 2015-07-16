#from lxml import etree

from xml.etree import cElementTree as ElementTree
import numpy as np
import sys

version = "{http://www.pnml.org/version-2009/grammar/pnml}"
#parser = etree.XMLParser(remove_blank_text=True)
class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def __str__(self):
        return str(self.__dict__)

class Arc:
    def __init__(self, pnml_id, source, target, value):
        self.pnml_id = pnml_id
        self.source = source
        self.target = target
        self.value = value

class Place:
    def __init__(self, pnml_id, name, initialmarking):
        self.name = name
        self.pnml_id = pnml_id
        self.initialmarking = initialmarking

class Transition:
    def __init__(self, pnml_id):
        self.pnml_id = pnml_id


class PNML_net:
    """
    Input :
    name : The name of the net
    places : A set of Place
    transitions : A set of Transition
    arcs : A set of Arc

    Variables :
    net : the numpy tuple reprensentation of the (Pre,Post) matrix
    P_map : maps the pnml_id of a Place with the row index of the numpy net
    T_map : maps the pnml_id of a Transition with the column index in the numpy net
    initialmarking : initial marking for the numpy representation of the net
    """   
    def __init__(self, name, places, transitions, arcs):
        self.name = name
        self.places = places
        self.transitions = transitions
        self.arcs = arcs
        self.generate_numpy_net()
    
    def generate_numpy_net(self) :

        p_size = len(self.places)
        t_size = len(self.transitions)
        pre = np.zeros(shape=(p_size,t_size))
        post = np.zeros(shape=(p_size,t_size))
        self.P_map = {}
        self.T_map = {}
        self.initialmarking = []

        for i,x in enumerate(self.places):
            self.P_map[x.pnml_id] = i
            self.initialmarking.append(x.initialmarking)
        self.initialmarking = np.array(self.initialmarking)

        for i,x in enumerate(self.transitions):
            self.T_map[x.pnml_id] = i
            
        for arc in self.arcs:
            if arc.source in self.P_map.keys():
              #  net['pre'][P[source]][T[target]] = int(list(list(a)[0])[0].text) #paresseux
                pre[self.P_map[arc.source]][self.T_map[arc.target]] = arc.value #paresseux
            elif arc.source in self.T_map.keys():
               # net['post'][P[target]][T[source]] = int(list(list(a)[0])[0].text)
                post[self.P_map[arc.target]][self.T_map[arc.source]] = arc.value
            else:
                raise Exception("The id of the arc's source is no where to be found.")

        self.net = np.rec.array(zip(pre.ravel(),post.ravel()), dtype=[('pre','uint'),('post','uint')]).reshape(pre.shape)

        

"""
Parse a .pnml file to a numpy representation. Some information of the pnml file will not be kept.

"""        
def parse(path):
    print('parsing {}...'.format(path))
    pnml_file = open(path,'r')
    # tree = etree.parse(pnml_file)
    it = ElementTree.iterparse(pnml_file)

    transitions = set()
    places = set()
    arcs = set()
    name = None

#    for event, el in it:
#        if event == 'end':
#            print(el.tag, el.attrib)
#            if el.tag == version + 'net':
#                name = el.findtext('{*}name/{*}text')

#            if el.tag == version + 'place':
#                initial_marking = int(el.findtext("{*}initialMarking/{*}text", 0))
#                pname = el.findtext("{*}name/{*}text")
#                places.add(Place(el.attrib['id'], pname, initial_marking))

#            elif el.tag == version + 'transition':
#                transitions.add(Transition(el.attrib['id']))

#            elif el.tag == version + 'arc':
#                arcs.add(Arc(el.attrib['id'], el.attrib['source'], el.attrib['target'], int(el.findtext("{*}inscription/{*}text", 1))))

#    print(name, places, transitions, arcs)

#    return PNML_net(name,places,transitions,arcs)

    root = it.root

    print(root.tag)
    page = root.find("net/page")
    name = root.findtext("net/name/text")

    for p in page.iter("place"):
        initial_marking = int(p.findtext("initialMarking/text", 0))
        pname = p.find("name/text").text
        places.add(Place( p.attrib['id'], pname, initial_marking))

    for t in page.iter("transition"):
        transitions.add(Transition(t.attrib['id']))

    for a in page.iter("arc"):
        # = Arc(pnml_id=a.attrib['id'],source=a.attrib['source'],target = a.attrib['target'])

        arcs.add(Arc(a.attrib['id'], a.attrib['source'], a.attrib['target'], int(a.findtext("inscription/text", 1))))

    return PNML_net(name,places,transitions,arcs)

#pnmls = []
#nets = []

#if __name__ == '__main__':
#    args = sys.argv
        
#    if len(args) == 1 :
#        print("No file specified. Feed me some .pnml files!")
#    else :
        #http://lxml.de/validation.html#relaxng
#        pnmlmodel = etree.parse(open('pnmlcoremodel.rng', 'r'))
#        grammar_validator = etree.RelaxNG(pnmlmodel)
    
#        for arg in args[1:]:


#            nets.append(parse(arg))

            
            
#            if grammar_validator(pnmlnet): #deconne. why???
#                pnmls.append(pnmlnet)
#                nets.append(parse_tree(pnml))        
#            else :
#                print("File "+arg+" could not be validated with PNML's core model grammar.")                  

