#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 15:45:54 2020

@author: mahsa

This is the Optimization file for the super-resolution project with signed inputs
"""

import numpy as np
import random
import os
import time
import swiglpk ##glpk mixed integer optimization package
import csv
import cvxpy as cp
from ProblemSpec import ProblemInit
from X_gen import X_generate
#from mip import Model, xsum, maximize, BINARY
import mosek



def optimization_function(A,X):
    S=ProblemInit()
    n=S.n
    m=S.m
    l=S.l
    L=S.L
    X_hat=np.zeros((n,1))
    data_signed=S.data_signed
    problem_type=S.PType
    B=np.zeros((n,L))
    Y_init=np.zeros((n,L))
    
    ####Test
    #X=np.abs(X)
    
    
    for index in range(0,n):
        loc=random.sample(range(L),l)
        B[index,loc]=1

    if data_signed==True:
        for j in range (0,L):
            B_vec=B[:,j]
            B_vec=np.reshape(B_vec,(n,1))
            Y_init[:,[j]]=np.multiply(B_vec,X)
        Y=np.matmul(A,Y_init)  
        
        ####Optimization using CVXPY, Ordinary Relaxed Problem 
        z=cp.Variable(shape=(n,1), nonneg= True)
        w=cp.Variable(shape=(n,L))
        constraints=[]
        constraints += [Y==cp.matmul(A,w)]
        constraints += [z>=0]

        for i1 in range (0,n):
            for i2 in range (0,L):
                constraints += [-z[i1]<= w[i1,i2]]
                constraints += [ w[i1,i2]<= z[i1]]
                #constraints += [ w[i1,i2]>=0]
       
        objective_func=cp.Minimize(cp.sum(z))        
        opt_problem=cp.Problem(objective_func,constraints)
        #opt_problem.solve(solver=cp.ECOS,eps=10**(-3),verbose=False,use_indirect=False)
        opt_problem.solve(solver=cp.ECOS)
        
        ####Optimization using two weights
        
        # z1=cp.Variable(shape=(n,1), nonneg= True)#positive parts
        # w1=cp.Variable(shape=(n,L))
        # w2=cp.Variable(shape=(n,L))

        # constraints1=[]
        # constraints1 += [Y==cp.matmul(A,(w1+w2))]
        # constraints1 += [z1>=0]        

        # for i1 in range (0,n):
        #     for i2 in range (0,L):
        #         constraints1 += [w2[i1,i2]<=0]
        #         constraints1 += [w2[i1,i2]>=-z1[i1]]
        #         constraints1 += [w1[i1,i2]<= z1[i1]]
        #         constraints1 += [w1[i1,i2]>=0]
                          
        # objective_func1=cp.Minimize(cp.norm(z1,p=1))        
        # opt_problem1=cp.Problem(objective_func1,constraints1)
        # opt_problem1.solve(solver=cp.SCS,gpu=False,eps=10**(-5),verbose=False,use_indirect=False)
                       
        # W1=np.array(w1.value)
        # W2=np.array(w2.value)
        # sum1=abs(np.sum(W1,axis=1))
        # sum2=abs(np.sum(W2,axis=1))
        # x_out1=z1.value
        # for i3 in range(0,n):
        #     if sum1[i3]>sum2[i3]:
        #         X_hat[i3]=x_out1[i3]
        #     else:
        #         if sum2[i3]>sum1[i3]:
        #             X_hat[i3]=-x_out1[i3]

        ####Uncomment the following for the ordinary relaxed problem
        x_out=z.value
        w_out=w.value

        summation=np.sum(w_out,axis=1)
        for i3 in range(0,n):
            if summation[i3]>=0:
                X_hat[i3]=x_out[i3]
            else:
                X_hat[i3]=-x_out[i3]
        
        ###comment this after testing for positive
        #X_hat=x_out
    
        
    if problem_type=='basic':
            Y_b=np.matmul(A,X)#X is signed 
            z_b=cp.Variable(shape=(n,1))
            constraint_b =[]
            constraint_b +=[Y_b==cp.matmul(A,z_b)]
            objective_func_b=cp.Minimize(cp.norm(z_b,p=1))        
            opt_problem_b=cp.Problem(objective_func_b,constraint_b)
            opt_problem_b.solve(solver=cp.SCS,gpu=False,eps=10**(-5),verbose=False,use_indirect=False)
            X_hat=z_b.value  
            
    if problem_type=='mixed_integer':
        
        for j in range (0,L):
            B_vec=B[:,j]
            B_vec=np.reshape(B_vec,(n,1))
            Y_init[:,[j]]=np.multiply(B_vec,X)
        Y=np.matmul(A,Y_init)
        print(Y_init)
        print(Y)
        z=cp.Variable(shape=(n,1), nonneg= True)
        w=cp.Variable(shape=(n,L))
        delta=cp.Variable(shape=(n,L),boolean=True)
        bigM=1000
        constraints=[]
        constraints += [Y==cp.matmul(A,w)]
        constraints += [z>=0]

        for i1 in range (0,n):
             for i2 in range (0,L):
                 constraints += [-bigM*(1-delta[i1,i2])<= w[i1,i2]]
                 constraints += [ w[i1,i2]<= bigM*delta[i1,i2]]
                 constraints += [w[i1,i2]<=z[i1]+bigM*(1-delta[i1,i2])]
                 constraints += [w[i1,i2]>=-z[i1]-bigM*delta[i1,i2]]
       
        objective_func=cp.Minimize(cp.sum(z))        
        opt_problem=cp.Problem(objective_func,constraints)
        #opt_problem.solve(solver=cp.GLPK_MI)###cp.GLPK_MI
        opt_problem.solve(solver=cp.MOSEK)###TESTING MOSEK ON CJ
        opt_problem.solve(solver = cp.MOSEK, 
                    mosek_params = {mosek.dparam.optimizer_max_time:  100.0,
                                    mosek.iparam.intpnt_solve_form:   mosek.solveform.free,

                                    },
                    verbose = True)
#                                      mosek.iparam.sim_max_iterations:  500.0,
#                                   mosek.iparam.intpnt_max_iterations: 200.0      
        
        
        
        x_out=z.value
        w_out=w.value
        summation=np.sum(w_out,axis=1)

        for i4 in range (n):
            sum_pos=0
            sum_neg=0
            for i5 in range(L):
                if w_out[i4,i5]>=0:
                    sum_pos=sum_pos+1
                else:
                    sum_neg=sum_neg+1
            if sum_pos>=sum_neg:
                X_hat[i4]=x_out[i4]
            else:
                X_hat[i4]=-x_out[i4]
            

        # for i3 in range(0,n):
        #     if summation[i3]>=0:
        #         X_hat[i3]=x_out[i3]
        #     else:
        #         X_hat[i3]=-x_out[i3]        
               
                           
    return X_hat

# ####Optimization using two variables
        
        # z1=cp.Variable(shape=(n,1), nonneg= True)#positive parts
        # z2=cp.Variable(shape=(n,1))#negative parts
        # w1=cp.Variable(shape=(n,L))
        # w2=cp.Variable(shape=(n,L))
        # constraints1=[]
        # constraints1 += [Y==cp.matmul(A,(w1+w2))]
        # constraints1 += [z1>=0]
        # constraints1 += [z2<=0]

        # for i1 in range (0,n):
        #     for i2 in range (0,L):
        #         constraints1 += [z2[i1]<= w2[i1,i2]]
        #         constraints1 += [w2[i1,i2]<=0]
        #         constraints1 += [ w1[i1,i2]<= z1[i1]]
        #         constraints1 += [w1[i1,i2]>=0]
        #         constraints1 += [z1[i1]>=z2[i1]]
        #         constraints1 += [w1[i1,i2]>=w2[i1,i2]]
        #         constraints1 += [z1[i1]>=w2[i1,i2]]
        #         constraints1 += [z2[i1]<=w1[i1,i2]]
                       
        # objective_func1=cp.Minimize(cp.norm(z1,p=1)+cp.norm(z2,p=1))        
        # opt_problem1=cp.Problem(objective_func1,constraints1)
        # opt_problem1.solve(solver=cp.SCS,gpu=False,eps=10**(-5),verbose=False,use_indirect=False)
                
        # x_out1=z1.value+z2.value
        # w_out1=w1.value+w2.value
        # X_hat=x_out1

####Optimization using PICOS, BIG M Problem
        
        #bigM = pic.Constant(10000)
        #z = pic.RealVariable("z", n)
        #w = pic.RealVariable("w", (n, L))  
        #b1 = pic.BinaryVariable("b1",(n,L)) 
        #b2 = pic.BinaryVariable("b2",(n,L)) 

        #prob=pic.Problem()
        #prob.add_constraint(z >= 0)
        #prob.add_constraint(Y == A*w)
        #for i1 in range (0,n):
        #    for i2 in range (0,L):
        #        prob.add_constraint( -bigM*(1-b1[i1,i2]) <= w[i1,i2] <= z[i1]+bigM*(1-b1[i1,i2]) )
        #       prob.add_constraint( -bigM*(1-b2[i1,i2])-z[i1] <= w[i1,i2]<= bigM*(1-b2[i1,i2]) )
        #       prob.add_constraint(b1[i1,i2]+b2[i1,i2]==1)
        #prob.set_objective("min", pic.sum(z))
        #prob.solve(solver="glpk")        
        #x_out=z.value
        #w_out=w.value
