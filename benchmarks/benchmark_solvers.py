#!/usr/bin/python
# -*- coding: utf-8 -*-
import benchmark
import math
import re #regex
import glob
import os


class Benchmark_Solver(benchmark.Benchmark):
    each = 1
    pass

def addtest(name, net, m0, m):
    def to_bench(self, net, m0, m, solver):
        print("trying "+str([net,m0,m,solver]))
        z = reachable(net,m0,m,solver=solver)
        print(name)
        print("From configuration")
        print(m0)
        print("To configuration")
        print(m)
        print(z)
    setattr(Benchmark_Solver, "test_qsoptex_" + name, lambda self: to_bench(self, net, m0, m,'qsopt-ex'))
    setattr(Benchmark_Solver, "test_z3_" + name, lambda self: to_bench(self, net, m0, m,'z3'))
    print("Added test_"+name)

if __name__ == '__main__':
    if __package__ is None:
  
        import sys
        from os import path
        sys.path.append(path.join(path.dirname(__file__), '..', 'src'))
        sys.path.append(path.join(path.dirname(__file__), '..', 'pnml'))
        import pnmlparser
        from generate_pn import getM2
        from algorithms import reachable
    args = sys.argv
    print(args)
    import pickle

    if len(args) == 1:
        print("No argument given. Running full test on .pnml in testset directory.")


        for filename in glob.glob(path.join(path.dirname(__file__),'testset/*.pnml')):

            x = raw_input("Do you wish to parse "+filename+"? (y/n)")
            if x != 'y':
                continue

            print("Parsing "+filename+" ...")
            #try:
            model = pnmlparser.parse(filename)
            m0 = model.initialmarking
            #except Exception as e :
            #    print(e.message)
            #    print("Failed to parse pnml")
            #    continue
            print("The size of the pnml is "+str(model.net.shape))
            x = raw_input("Do you wish to generate a final marking? (y/n)")
            if x == 'y':

                print("Generating final marking...")
    #           m = getM(pnml.net.shape[0])
                setattr(model,'finalmarking',getM2(model.net,m0,0.2))
                m=model.finalmarking
                print(model.name,"\n",m0,m)
                #if verbose : print()

                pickle.dump(model, open(model.name+'.nPN',"wb"))
                print("Saved "+model.name+".nPN")


            #def to_bench(self, net, m0, m):
            #    z = reachable(net,m0,m,solver=self.solver)
            #    print(z)
            #print("Adding to benchmark class")
            #setattr(Benchmark_Solver,"test_"+pnml.name, lambda self : to_bench(self.solver, pnml.net,pnml.initialmarking,m))

        x = raw_input("Do you wish to run test on every .nPN files in testset/ ? (y/n)")
        if x == 'y':
            for filename in glob.glob(path.join(path.dirname(__file__),'testset/*.nPN')):

                model = pickle.load(open(filename,"rb"))
                addtest(model.name,model.net,model.initialmarking,model.finalmarking)
    else:

        #Takes .npn file. which is basically load with pickle and use the attributes
        for arg in args[1:]:
  #          pnmlregex = re.compile("*.pnml")
 #           npnregex = re.compile("*.nPN")

#            if pnmlregex.match(arg) :
                #parsepnml
            #Must be a .nPN
            model = pickle.load(open(arg,"rb"))
            addtest(model.name,model.net,model.initialmarking,model.finalmarking)


    r = Benchmark_Solver()
    r.run()
#    r = benchmark.main(format="csv", numberFormat="%.4g")
    x = r.getTable(format='csv')
    x = x.replace(' ','')
    x = x.replace('|',',')
    x = x.split('\n')
    print(r)
    previous_result = open('result.csv',"rb").read()
    for i in range(1,len(x)):
        previous_result += '\n'+x[i]
    print(previous_result)
    f = open('result.csv',"wb")
    f.write(previous_result)
    f.close()
