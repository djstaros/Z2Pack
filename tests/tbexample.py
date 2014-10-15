#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    15.10.2014 10:22:43 CEST
# File:    tbexample.py

import sys
sys.path.append('../src')
import z2pack

from common import *

import types
import unittest


class TbExampleTestCase(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(TbExampleTestCase, self).__init__(*args, **kwargs)
        self.assertIterAlmostEqual = types.MethodType(assertIterAlmostEqual, self)
        self.assertContainerAlmostEqual = types.MethodType(assertContainerAlmostEqual, self)
    
    def setUp(self):
        t1 = 0.2
        t2 = 0.3
        
        self.H = z2pack.tb.Hamilton([1, 0, 0], [0, 1, 0], [0, 0, 1])
    
        # create the two atoms
        self.H.add_atom(([1, 1], 1), [0, 0, 0])
        self.H.add_atom(([-1, -1], 1), [0.5, 0.5, 0])
        
        # add hopping between different atoms
        self.H.add_hopping( ((0, 0), (1, 1)), 
                            z2pack.tb.vectors.combine([0,-1],[0,-1],0), 
                            t1, 
                            phase = [1, -1j, 1j, -1])
        self.H.add_hopping( ((0, 1), (1, 0)), 
                            z2pack.tb.vectors.combine([0,-1],[0,-1],0), 
                            t1, 
                            phase = [1, 1j, -1j, -1])
        
        # add hopping between neighbouring orbitals of the same type
        self.H.add_hopping( (((0, 0), (0, 0)),((0, 1), (0, 1))), 
                            z2pack.tb.vectors.neighbours([0,1]), 
                            t2, 
                            phase = [1])
        self.H.add_hopping( (((1, 1), (1, 1)),((1, 0), (1, 0))), 
                            z2pack.tb.vectors.neighbours([0,1]), 
                            -t2, 
                            phase = [1])
        
    def test_res(self):
        # call to Z2Pack
        tb_system = z2pack.tb.System(self.H)
        tb_plane = tb_system.plane(1, 2, 0)
        tb_plane.wcc_calc(verbose = False, num_strings=20, use_pickle = False)
        self.assertContainerAlmostEqual(tb_plane.get_res(), ([0.0,
        0.026315789473684209, 0.052631578947368418, 0.078947368421052627,
        0.10526315789473684, 0.13157894736842105, 0.15789473684210525,
        0.18421052631578946, 0.21052631578947367, 0.23684210526315788,
        0.26315789473684209, 0.28947368421052633, 0.31578947368421051,
        0.34210526315789469, 0.36842105263157893, 0.39473684210526316, 
        0.42105263157894735, 0.44736842105263153, 0.47368421052631576, 0.5], [[
        0.49983964546467036, 0.50016035453532992], [0.49890749383729088, 
        0.50109250616270917], [0.49641395036486252, 0.50358604963513764], [
        0.49554883941587446, 0.50445116058412554], [0.49652567629394373, 
        0.5034743237060566], [0.49208434055431727, 0.50791565944568262], [
        0.48929271594465651, 0.51070728405534349], [0.48629705364229231, 
        0.51370294635770786], [0.48144595206989665, 0.5185540479301034], [
        0.47656990584661874, 0.52343009415338138], [0.46885604857621033, 
        0.53114395142378967], [0.45994586240888752, 0.54005413759111265], [
        0.44382468776376022, 0.55617531223623984], [0.42063176788723156, 
        0.57936823211276867], [0.3819089388751013, 0.61809106112489864], [
        0.32658906586480313, 0.67341093413519704], [0.24624568378330641, 
        0.75375431621669375], [0.15953456444997946, 0.8404654355500204], [
        0.081400024690988546, 0.9185999753090115], [0.0038664353524984719, 
        0.99613356464750147]], [0.0, 0.0, 0.0, 0.0, 2.2204460492503131e-16, 0.0
        , 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 
        0.49999999999999989, 0.5, 0.5])
) 

if __name__ == "__main__":
    unittest.main()
    