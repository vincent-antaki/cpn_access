#!/usr/bin/python
# -*- coding: utf-8 -*-

from algorithms import *

import benchmark
from generate_pn import *
import math
import re #regex


class Benchmark_Solver(benchmark.Benchmark):

    each = 1 # allows for differing number of runs

    def setUp(self):
        self.solver='qsopt-ex'        
            
class Benchmark_z3(Benchmark_Solver):
    def setUp(self):
        self.solver = 'z3'


if __name__ == '__main__':
    if __package__ is None:
        print("a")
        import sys
        from os import path
        sys.path.append(path.dirname( path.abspath(__file__)) )
        print(__package__)
        from ..pnml import pnmlparser 
        
    pnmlregex = re.compile(".*\.pnml")
    args = sys.argv
    
    for arg in args[2:]:
        if pnmlregex.match(arg) :
            #parsepnml
            pnml = parse_pnml(arg)
            setattr(Benchmark_Solver,"test_"+pnml.name, lambda self:reachable(pnml.net,self.m0,getM(pnml.net)))
            
        else :
            print("Not a pnml")     

    benchmark.main(format="markdown", numberFormat="%.4g")
    # could have written benchmark.main(each=50) if the
    # first class shouldn't have been run 100 times.
