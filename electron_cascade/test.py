# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 18:30:48 2020

@author: chelsea
"""

def getsort(processes):
    
    import numpy as np

    y = np.zeros((np.size(processes,0),1))
    
    for ii in range(np.size(processes,0)):
        for jj in range(np.size(processes[ii,:])):
            y[ii] = y[ii] + 10**jj*abs(processes[ii,-(jj+1)])
            
    return y