# -*- coding: utf-8 -*-
"""
Created on Thu May 14 13:53:31 2020

@author: chelsea
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_state_prob(psi_t, total_time, dt, ES):
    
    COLORS = ['r', 'b', 'm', 'g', 'k', 'c', 'y']
    LINE = ['-', '--', '-.', ':']
    
    plt.figure()
    
    for ii in range(np.size(psi_t,0)):
        plt.plot(np.linspace(0, int(total_time/dt)*dt, int(total_time/dt)), psi_t[ii,:], \
                 label = str(ES[ii,:]), color = COLORS[ii%len(COLORS)], linestyle = LINE[ii%len(LINE)])
        
    plt.legend()
    plt.xlabel('fs')
    plt.ylabel('probability')