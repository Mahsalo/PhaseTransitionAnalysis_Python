#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 14:38:25 2020
@author: mahsa
"""
import numpy as np
from numpy import linalg as LA
import random
#import torch
#import cvxpy as cp
import csv
import pandas as pd
import os
from numpy import empty
import glob
import sys, argparse
from collections import defaultdict
import os.path

#n=100###total number of the folders, 99
n=50
dir_name='/Users/mahsa/Desktop/Post_Doc_Research/MyProjects/BEAM_Imaging/BEAM_Python_Codes/Python_Results_July/mosek_results/n50L10ll3'
#dir_name='/Users/mahsa/Desktop/Post_Doc_Research/MyProjects/Covid_project/Covid_multiscale_CS/phase_tr_covid'###for the basic problem

filename_suffix = 'txt'
indicator=0
M=30;

for i in range (1,n+1):
    #cat 'result_cvxpy.txt' | tr -d '()' > 'result_cvxpy.txt'
    if i>=1:
        if i==1:
            P1=empty([1,M]);

        f1=open('rho.csv','a',newline='')
        f2=open('delta.csv','a',newline='')
        f3=open('srate.csv','a',newline='')
        f4=open('kappa.csv','a',newline='')

        writer_rho=csv.writer(f1)
        writer_delta=csv.writer(f2)
        writer_srate=csv.writer(f3)
        writer_kappa=csv.writer(f4)

    base_foldername=str(i)
    base_filename='result_cvxpy'
    path=os.path.join(dir_name, base_foldername,base_filename+'.'+'txt' )
    path_origin=os.path.join(dir_name)
    FileCheckFlag=os.path.isfile(path) 

    if FileCheckFlag==True:##if the results are written in the text file or the csv file
        fout1=open('results.txt','a')
        fout2=open(path)

        for line in fout2:
            fout1.write(line)
            
        os.system('cat "results.txt" | tr -d "()" > "output_all.txt" ')   
        fout1.close()  
        fout2.close()
        
        my_csv_results = pd.read_csv(path,header=None,delim_whitespace=True).values##array of values  
        indicator=indicator+1##Number of existing csv files
        delta=my_csv_results[:,6]###delta=m/n 7th
        rho=my_csv_results[:,5]##rho=k/m one 6th
        k=my_csv_results[:,2]##this is just the sparsity value 
        srate=my_csv_results[:,7]##success rate last element        
        L=my_csv_results[:,0]
        l_small=my_csv_results[:,1]
        it=my_csv_results[:,4]##iterations
              
        res_array=np.zeros((len(k),7))
        kappa=np.zeros((len(k),1))
        for i1 in range (len(k)):##This loop is required to find the Kappa values
            delta[i1]=delta[i1].replace(",","")
            L[i1]=L[i1].replace("(","")
            L[i1]=L[i1].replace(",","")
            l_small[i1]=l_small[i1].replace(",","")
            rho[i1]=rho[i1].replace(",","")
            srate[i1]=srate[i1].replace(")","")
            k[i1]=k[i1].replace(",","") 
            it[i1]=it[i1].replace(",","")
            kappa[i1]=int(k[i1])/(n+1)

        os.chdir(path_origin) # set working directory        
        writer_rho.writerow(list(rho))
        writer_delta.writerow(list(delta))
        writer_srate.writerow(list(srate))
        writer_kappa.writerow(list(kappa))
                
        f1.close()
        f2.close()
        f3.close()
        f4.close()

print(indicator)      