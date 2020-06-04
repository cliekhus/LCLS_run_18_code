# -*- coding: utf-8 -*-
"""
Created on Fri May 29 11:50:55 2020

@author: chelsea
"""

import numpy as np
import matplotlib.pyplot as plt


M = np.loadtxt('C:/Users/chelsea/OneDrive/Documents/UW/Mixed-Valence-Complexes/LCLSrun18/Calculations/feru-m0.roots',comments='#')

def broaden(roots):
    
    EV = np.linspace(6965, 6980, 10000)
    XANES = np.zeros(np.size(EV))
    width = .5
    
    for root in roots:
        XANES = XANES + root[1]*np.exp(-(EV-root[0])**2/2/width**2)
        
    return EV, XANES


EV, XANES = broaden(M)

plt.figure()

plt.stem(M[:,0], M[:,1])
plt.plot(EV, XANES)



        