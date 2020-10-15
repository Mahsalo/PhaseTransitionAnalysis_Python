#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 10:47:49 2020

@author: mahsa

Initialization Routine for super-resolution with signed entry
"""

import numpy as np
from numpy import linalg as LA
import random
import csv
 
def ProblemInit():
    class ProbInit:
        def __init__(self):
            self.n=20;
            self.L=5;
            self.l=3;
            self.Monte_Carlo_iter=20;##The number of times that we test our resconstruction algorithm for each specific (k,m,n) tuple
            self.error_threshold=10**(-2)
            self.data_signed=False;###must be true for relaxed form
            self.m=np.linspace(2,self.n,self.n-1)
            self.mu=0.0
            self.sigma=1
            self.PType="mixed_integer"#'mixed_integer'#'mixed_integer';##'basic'
    Init=ProbInit();
    
    return Init;
   
