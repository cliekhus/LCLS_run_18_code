# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 18:30:48 2020

@author: chelsea
"""

import numpy as np

LW_R = 0.35*1000
LW_A = 0.8*1000

Psi_0 = np.array([1,0,0])

Psi = Psi_0

for ii in range(10000):
    Psi = Psi + np.array([-1/LW_R*Psi[0]-1/LW_A*Psi[0], 1/LW_R*Psi[0], 1/LW_A*Psi[0]])