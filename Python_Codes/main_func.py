#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 10:11:46 2019
@author: mahsa
"""
import numpy as np
from numpy import linalg as LA
import random
import csv
from ProblemSpec import ProblemInit
from loop import inner_loop
from X_gen import X_generate
from opt_func import optimization_function

S=ProblemInit()
m=S.m
L=S.L
#for i in range(len(m)): This does not work with ClusterJob just remember! 

for i in range(19):              
    inner_loop(int(L),int(m[i]))
    
