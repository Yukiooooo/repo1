#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 17:27:32 2021

this is shit
This code is used for testing Qingyu Zhu's python code
@author: yxh5920
"""
# Import shit.  I needed a lot of shit this time.  
import numpy as np                                                             
import matplotlib                                                              
matplotlib.use('Agg')                                                          
import matplotlib.pyplot as plt

from glob import glob                                                          
from scipy.io import readsav                                                   
import os
from apexpy import Apex
import datetime as dt

A = Apex(date=2015.3,refh=110.)

sat_key='sim_lab'

data_pt='./'+sat_key+'/n5/'

save_pt='./'

if not os.path.exists(save_pt):
    os.makedirs(save_pt)

data_dir=data_pt                                                       
flist=sorted(glob(data_dir+'*.sav'));nfile=len(flist)

print (data_dir,len(flist),nfile)

for ifile, fname in enumerate(flist[:1]):

    sav_data = readsav(fname)                                                  
    lon=sav_data['lon'][2]/np.pi*180.                                        
    lat=sav_data['lat'][2]/np.pi*180.
    alt=sav_data['alt'][2:-2]/1000.

nalt=len(alt)
all_parm1=np.zeros([nfile,nalt])
all_parm2=np.zeros([nfile,nalt])
all_parm3=np.zeros([nfile,nalt])
all_parm4=np.zeros([nfile,nalt])

all_parm5=np.zeros([nfile,nalt])

ut=np.zeros(nfile)
glon=np.zeros(nfile)
glat=np.zeros(nfile)
mlt=np.zeros(nfile)
mlat=np.zeros(nfile)

time_st1=dt.datetime(2015,3,17) # need to change everytime

ialt=np.argmin(abs(alt-350.));print (ialt,alt[ialt])

for ifile, fname in enumerate(flist[:]):

    sav_data = readsav(fname)
    time1=sav_data['itime1']

    #ut[ifile]=(time1[2]-2)*24.+time1[3]+time1[4]/60.+time1[5]/3600.
    #print (ut[ifile])

    time2=dt.datetime(int(time1[0]),int(time1[1]), int(time1[2]),
                      int(time1[3]),int(time1[4]), int(time1[5]))

    
    lon=sav_data['lon'][2]/np.pi*180.                                          
    lat=sav_data['lat'][2]/np.pi*180. 
    
    glon[ifile]=lon
    glat[ifile]=lat

    dtime1=time2-time_st1
    
    ut[ifile]=dtime1.days*24+dtime1.seconds/3600.
    
    mlat[ifile], mlt[ifile] = A.convert(glat[ifile], glon[ifile], 
                                        'geo', 'mlt',datetime=time2, 
                                        height=alt[ialt])

    #print (ut[ifile],mlat[ifile],mlt[ifile])

    parm=sav_data['Veast'][2:-2]
    all_parm1[ifile,:]=parm[:]

    parm=sav_data['Vnorth'][2:-2]
    all_parm2[ifile,:]=parm[:]

    parm=sav_data['Vup'][2:-2]
    all_parm3[ifile,:]=parm[:]

    parm=sav_data['Rho'][2:-2]                                                
    all_parm4[ifile,:]=parm[:]

    parm=sav_data['Eden'][2:-2]                                                
    all_parm5[ifile,:]=parm[:] 

    #print(ifile,all_parm3[ifile,ialt])

save_fn=save_pt+'20150317_n5glon'
np.savez(save_fn,ut=ut,glon=glon,glat=glat,alt=alt,mlat=mlat,mlt=mlt,
         V1=all_parm1[:,:],V2=all_parm2[:,:],
         V3=all_parm3[:,:],rho=all_parm4[:,:],eden=all_parm5[:,:])

print ("=> File saved:",save_fn)    

