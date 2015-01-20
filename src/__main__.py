import PetriNet as pn
import cpn_analysis as cpn
import numpy as np

pn.test()
net = pn.getTestPetriNet()

z = cpn.fireable(net ,np.array([4,3,4]),np.array([0,1]))

w = cpn.reachable(net, np.array([4,3,4]),np.array([10, 20, 15]))

print(z)
print(w)
        

