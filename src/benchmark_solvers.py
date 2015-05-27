#!/usr/bin/python
# -*- coding: utf-8 -*-

from algorithms import *

import benchmark
from generate_pn import _load
import math

class Benchmark_Solver(benchmark.Benchmark):

    each = 1 # allows for differing number of runs
    testsets = {i:_load(i) for i in ['verysmall','small','medium','big','huge','gigantic']}

    def setUp(self):
        self.solver='qsopt-ex'        
        
    def test_very_small_set(self):
        print("verysmall ", self.solver)
        for net,m0,m in self.testsets['verysmall']:
            print(reachable(net,m0,m,self.solver))   

    def test_small_set(self):
        print("small ", self.solver)
        for net,m0,m in self.testsets['small']:
            print(reachable(net,m0,m,self.solver))  
 
    def test_medium_set(self):
        print("medium ", self.solver)
        for net,m0,m in self.testsets['medium']:
            print(reachable(net,m0,m,self.solver))  
#            pass
              
    def test_big_set(self):
        print("big ", self.solver)
        for net,m0,m in self.testsets['big']:
            print(reachable(net,m0,m,self.solver))  
#            pass

    def test_huge_set(self):
        print("huge ", self.solver)
        for net,m0,m in self.testsets['huge']:
            print(reachable(net,m0,m,self.solver))  
            pass
            
    def test_gigantic_set(self):
        print("gigantic ", self.solver)
        for net,m0,m in self.testsets['gigantic']:
            print(reachable(net,m0,m,self.solver))  
            pass
            
class Benchmark_z3(Benchmark_Solver):
    def setUp(self):
        self.solver = 'z3'


if __name__ == '__main__':
    pass
    benchmark.main(format="markdown", numberFormat="%.4g")
    # could have written benchmark.main(each=50) if the
    # first class shouldn't have been run 100 times.
