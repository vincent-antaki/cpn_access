import petrinet as pn
from algorithms import reachable, fireable
import numpy as np

petrinet = np.matrix([
        [(2, 0), (0, 0), (3, 8), (1, 2), (0,37)],
         [(0, 3), (1, 3), (5, 0), (5, 2), (23,0)]],
         dtype=[('pre', 'uint'), ('post', 'uint')])
         
a = np.matrix(
               [[(1,0), (1,3), (0,1), (1,0)],
                [(1,1), (2,0), (0,0), (0,0)],
                [(0,0), (0,1), (1,0), (0,1)]],
        dtype=[('pre', 'uint'), ('post', 'uint')])

#print("net:", petrinet)
#print("preset:", pn.preset(petrinet, [2]))
#print("postset:", pn.postset(petrinet, [1]))
#print("reversed", pn.reversed_net(petrinet))
#print("subnet:", pn.subnet(petrinet, [1, 3]))
#print("subnet:", pn.subnet(petrinet, [1, 3], True))
