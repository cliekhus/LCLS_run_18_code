# -*- coding: utf-8 -*-
"""
Created on Thu May 14 13:53:31 2020

@author: chelsea
"""

import numpy as np
import matplotlib.pyplot as plt

COLORS = ['r', 'b', 'm', 'g', 'k', 'c', 'y']
LINE = ['-', '--', '-.', ':']

def plot_state_prob(psi_t, total_time, dt, ES):
    
    plt.figure()
    
    for ii in range(np.size(psi_t,0)):
        plt.plot(np.linspace(0, int(total_time/dt)*dt, int(total_time/dt)), psi_t[ii,:], \
                 label = str(ES[ii,:]), color = COLORS[ii%len(COLORS)], linestyle = LINE[ii%len(LINE)])
        
    plt.legend()
    plt.xlabel('fs')
    plt.ylabel('probability')
    
def plot_charge_prob(psi_t, total_time, dt, ES):
    
    charges = np.array([ES[:,0], np.sum(ES[:,[1,2,3]],1), np.sum(ES[:,[4,5,6,7]],1)])
    
    unique_charges = np.unique(charges,axis=1)
    
    charges_t = np.zeros((np.shape(unique_charges)[1],np.shape(psi_t)[1]))
    
    for ii in range(np.shape(unique_charges)[1]):
        for jj in range(np.shape(charges)[1]):
            if (unique_charges[:,ii] == charges[:,jj]).all():
                charges_t[ii,:] = charges_t[ii,:] + psi_t[jj,:]
    
    plt.figure()
    
    for ii in range(np.size(charges_t,0)):
        plt.plot(np.linspace(0, int(total_time/dt)*dt, int(total_time/dt)), charges_t[ii,:], \
                 label = str(unique_charges[:,ii]), color = COLORS[ii%len(COLORS)], linestyle = LINE[ii%len(LINE)])
        
    plt.legend()
    plt.xlabel('fs')
    plt.ylabel('probability')
    
    
    
    
    charges = np.sum(ES,1)
    
    unique_charges = np.unique(charges)
    
    charges_t = np.zeros((np.shape(unique_charges)[0],np.shape(psi_t)[1]))
    
    for ii in range(np.shape(unique_charges)[0]):
        for jj in range(np.shape(charges)[0]):
            if (unique_charges[ii] == charges[jj]).all():
                charges_t[ii,:] = charges_t[ii,:] + psi_t[jj,:]
    
    plt.figure()
    
    for ii in range(np.size(charges_t,0)):
        plt.plot(np.linspace(0, int(total_time/dt)*dt, int(total_time/dt)), charges_t[ii,:], \
                 label = str(unique_charges[ii]), color = COLORS[int(-unique_charges[ii]-1)], linestyle = LINE[ii%len(LINE)])
        
    plt.legend()
    plt.xlabel('fs')
    plt.ylabel('probability')
  
    
    
def plot_distribution(psi, ES):
    
    PATTERNS = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O", ".", "*" ]
    
    index = np.argsort(psi)
    index = np.flip(index)
    
    plt.figure()
    
    total_prob = 0
    ii=1
    while total_prob < .5:
        prob =  psi[index[ii-1]]
        
        ES_choice = ES[index[ii-1],:]
        ES_label = 0
        for jj in range(np.size(ES_choice)):
            ES_label = ES_label + 10**jj*abs(ES_choice[-(jj+1)])

        plt.bar(ii, prob, color = COLORS[int(-sum(ES_choice)-1)], hatch = PATTERNS[(ii-1)%len(PATTERNS)], label = str(ii) + ': ' + str(int(ES_label)).zfill(8))
        plt.legend()
        
        ii+=1
        
        total_prob += prob
        
        
        
        
        
        
        
        
        
        
        
        