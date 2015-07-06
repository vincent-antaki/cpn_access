#!/usr/bin/python
# -*- coding: utf-8 -*-
import benchmark
import math
import re #regex
import glob
import os


class Benchmark_Solver(benchmark.Benchmark):

    each = 1 # allows for differing number of runs

    def setUp(self):
        self.solver='qsopt-ex'        

def addtest(name, net, m0, m):
    def to_bench(self, net, m0, m):
        z = reachable(net,m0,m,solver=self.solver)
        print(name)
        print("From configuration")
        print(m0)
        print("To configuration")
        print(m)
        print(z)
    setattr(Benchmark_Solver, "test_" + name, lambda self: to_bench(self, net, m0, m))
    print("Added test_"+name)


class Benchmark_z3(Benchmark_Solver):
    def setUp(self):
        self.solver = 'z3'

if __name__ == '__main__':
    if __package__ is None:
  
        import sys
        from os import path
        sys.path.append(path.join(path.dirname(__file__), '..', 'src'))
        sys.path.append(path.join(path.dirname(__file__), '..', 'pnml'))
        import pnmlparser
        from generate_pn import getM2
        from algorithms import reachable
    pnmlregex = re.compile(".*\.pnml")
    args = sys.argv
    print(args)
    if len(args) == 1:
        import pickle
        print("No argument given. Running full test on .pnml in testset directory.")


        for filename in glob.glob(path.join(path.dirname(__file__),'testset/*.pnml')):

            x = raw_input("Do you wish to parse "+filename+"? (y/n)")
            if x != 'y':
                continue

            print("Parsing "+filename+" ...")
            try:
                pnml = pnmlparser.parse(filename)
                m0 = pnml.initialmarking
            except Exception as e :
                print(e.message)
                print("Failed to parse pnml")
                continue
            print("The size of the pnml is "+str(pnml.net.shape))
            x = raw_input("Do you wish to generate a final marking? (y/n)")
            if x == 'y':

                print("Generating final marking...")
    #           m = getM(pnml.net.shape[0])
                setattr(pnml,'finalmarking',getM2(pnml.net,m0,0.2))
                m=pnml.finalmarking
                print(pnml.name,"\n",m0,m)
                #if verbose : print()

                pickle.dump(pnml, open(pnml.name+'.nPN',"wb"))
                print("Saved "+pnml.name+".nPN")


            #def to_bench(self, net, m0, m):
            #    z = reachable(net,m0,m,solver=self.solver)
            #    print(z)
            #print("Adding to benchmark class")
            #setattr(Benchmark_Solver,"test_"+pnml.name, lambda self : to_bench(self.solver, pnml.net,pnml.initialmarking,m))

        for filename in glob.glob(path.join(path.dirname(__file__),'testset/*.nPN')):

            pnml = pickle.load(open(filename,"rb"))
            addtest(pnml.name,pnml.net,pnml.initialmarking,pnml.finalmarking)
    else:
        for arg in args[1:]:
            if pnmlregex.match(arg) :
                #parsepnml
                pnml = pnmlparser.parse(arg)
                m0 = pnml.initialmarking
#               m = getM(pnml.net.shape[0])
	        m = getM2(pnml.net,m0,0.2)

                setattr(Benchmark_Solver,"test_"+pnml.name, lambda self:reachable(pnml.net,pnml.initialmarking,m,solver=self.solver))             
            else :
                print("Not a pnml")     

    benchmark.main(format="markdown", numberFormat="%.4g")
    # could have written benchmark.main(each=50) if the
    # first class shouldn't have been run 100 times.
