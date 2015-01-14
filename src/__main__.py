import PetriNet as pn
import cpn_analysis as cpn
import numpy as np

#pn.petrinet_test()
a = pn.getTestPetriNet()
z = cpn.fireable(a,np.array([4,3,4]),[0,1])
print(z)
        

