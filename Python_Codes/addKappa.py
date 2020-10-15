#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 17:23:18 2020

@author: mahsa
"""
import numpy as np
import pandas as pd
import os

#dir_name='/Users/mahsa/Desktop/Post_Doc_Research/MyProjects/BEAM_Imaging/BEAM_Python_Codes/Python_Results_July/L10l4'
#dir_name='/Users/mahsa/Desktop/Post_Doc_Research/MyProjects/Covid_project/Covid_multiscale_CS/phase_tr_covid'###for the basic problem
dir_name='/Users/mahsa/Desktop/Post_Doc_Research/MyProjects/BEAM_Imaging/BEAM_Python_Codes/Python_Results_July/mosek_results/n50L10ll3'

os.chdir(dir_name)
Data=pd.read_csv('output_all.txt',names=["L_Capital","l_small","k","m","it","rho","delta","success"])
k=Data.iloc[:,2]
n=50
kappa=k/n
Data_new=Data.assign(kappa=kappa)

Data_new.to_csv('modified_output.txt',index=False)
