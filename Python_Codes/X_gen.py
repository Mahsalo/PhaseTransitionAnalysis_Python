#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 14:53:10 2020

@author: mahsa
"""

import numpy as np
import random
from ProblemSpec import ProblemInit

def X_generate(n,k):
    S=ProblemInit()  
    X=np.zeros((n,1))
    Xi=np.ones((n,1))
    data_signed=S.data_signed
    nonzero_loc=random.sample(range(n),k)##gives k random values 0<=x<=n-1 
    for i in range(len(nonzero_loc)):
        X[nonzero_loc[i]]=10*np.abs(np.random.normal(S.mu,S.sigma,1))
    if  k>1:
        half_nonz=int(np.floor(k/2))
        neg_index=random.sample(nonzero_loc,half_nonz)
        Xi[neg_index]=-1
    if  k==1:
        Xi[nonzero_loc]=-1
    X_out=X*Xi
        
    return X_out