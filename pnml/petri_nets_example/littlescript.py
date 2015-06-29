                
for filename in os.listdir(os.getcwd()): 
    if 'PT' in os.listdir(filename):
        for f in glob.glob(filename+'/PT/*.pnml'):
            x = f.split('/')
            x = x[len(x)-1]
            os.rename(f,'testset/'+x)            

