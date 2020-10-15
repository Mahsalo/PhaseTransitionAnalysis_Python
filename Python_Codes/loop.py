#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 14:15:02 2020

@author: mahsa
Inner loop subroutine for super-resolution project
"""

import numpy as np
from numpy import linalg as LA
import random
import csv
import time
from ProblemSpec import ProblemInit
from X_gen import X_generate
from opt_func import optimization_function

def inner_loop(L,m):
    
   S=ProblemInit()
   n=S.n
   L=S.L
   l=S.l
   it=S.Monte_Carlo_iter
   mu=S.mu
   sigma=S.sigma
   
   for k in range (1,n+1):
       A=np.random.normal(mu, sigma, (m,n))
       if k==1:
          Success=np.zeros((it,1))

       for i in range (0,it):
           X=X_generate(n,k)
           
           ##comment this after trying positive values
           #X=np.abs(X)

           X_hat=optimization_function(A,X)
           err=LA.norm(X-X_hat,2)/LA.norm(X,2)
           if err <= S.error_threshold:
               Success[i]=1
           print("X",X)
           print("Xh",X_hat)
       success_rate=np.sum(Success)/it        
       output=L,l,k,m,it,k/m,m/n,success_rate

       outF=open("result_cvxpy.txt","a+")
       outF.writelines(str(output)+"\n")
       outF.close()
       
       if i==(it-1):
          Success=np.zeros((it,1))
          err=0
          success_rate=0
       
  