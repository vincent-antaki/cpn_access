import glob
import os

"""
For all directories x in current directory, this script take all .pnml files in x/PT/*.pnml and put them in directory 'testset'. testset must already exist.
"""
for filename in filter(os.path.isdir,os.listdir(os.getcwd())): 
    
    if 'PT' in os.listdir(filename):
        for f in glob.glob(filename+'/PT/*.pnml'):
            x = f.split('/')
            x = x[len(x)-1]
            os.rename(f,'testset/'+x)            

