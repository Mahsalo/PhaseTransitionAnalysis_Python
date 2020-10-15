#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 12:26:16 2020

@author: mahsa
"""
import numpy as np
import csv
import pandas as pd
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm
import random

#filename='/Users/mahsa/Desktop/Post_Doc_Research/MyProjects/Covid_project/Covid_multiscale_CS/phase_tr_covid/logit_fit.txt'
filepath='/Users/mahsa/Desktop/Post_Doc_Research/MyProjects/BEAM_Imaging/BEAM_Python_Codes/Python_Results_July/mosek_results/n50L10ll3/modified_output.txt'
filename='/Users/mahsa/Desktop/Post_Doc_Research/MyProjects/BEAM_Imaging/BEAM_Python_Codes/Python_Results_July/mosek_results/n50L10ll3/logit_fit.txt'


data=pd.read_csv(filepath)
kappa=data.iloc[1:,8]
success=data.iloc[1:,7]
delta=data.iloc[1:,6]

uni_delta=delta.unique()
indicator=1
for i in range(len(uni_delta)):
    ind=np.where(delta==uni_delta[i])
    X=kappa.iloc[ind]
    Y=success.iloc[ind]
    sh=pd.DataFrame(ind).shape
    X=X.values.reshape((sh[1],1))
    Y=Y.values.reshape((sh[1],1))
    X1 = sm.add_constant(X)
    mod = sm.GLM(Y,X1,family=sm.families.Binomial(link=sm.families.links.logit))
    if len(np.unique(Y))>2:##If Y has only two values there would be Perfect Separation Error
        fitted=mod.fit()
        pars=fitted.params
        kappa_half=-pars[0]/pars[1]
        
        df=pd.DataFrame([uni_delta[i]],[kappa_half])##columns are in wrong order, kappa, delta
        if indicator==1:
            file=open(filename,'w')
            df.to_csv(file,mode='w',header=False)
            file.close()
        else:
            file=open(filename,'a')
            df.to_csv(file,mode='a',header=False)
            file.close()
        indicator +=1
     
