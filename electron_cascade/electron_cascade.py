# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:06:55 2020

@author: chels
"""

import numpy as np
from make_electronic_states import make_elec_states
import pickle


def coupling_term(i, j, coeff, size): #coeff in fs^-1
    
    delta_U = np.zeros((size, size))
    
    delta_U[i,i] = -coeff
    delta_U[j,i] = coeff
    
    return delta_U


def make_U(M, size, dt): #dt in fs
    
    U = np.eye(size)
    
    for line in M:
        #dt/line[2]*line[3]

        U += coupling_term(int(line[0]), int(line[1]), dt/line[2]*line[3], size)
        
    return U


def make_psi_0(size):
    psi = np.zeros((size))
    psi[0] = 1
    
    return psi
    

def main(run_new_es):
        
    
    TOTAL_TIME = 1 #fs
    DT = .001 #fs
    
    if run_new_es:
        ES, M = make_elec_states(True)
    else:
        with open("electronic_states.pkl", "rb") as f:
            ES = pickle.load(f)
        with open("decay_pathway.pkl", "rb") as f:
            M = pickle.load(f)
    
    Y = np.array([1.14,1.12,1.12,1.02,1.01,1.01,1,1.14,1.14,1.04,1.03,1.03,1.02,1.02,1.14,1.04,1.03,1.03,1.02,1.02,1.14,1.13,1.13,1.12,1.14,1.14,1.13,1.13,1.14,1.13,1.13])
    #Y = 6/Y
    M[:,2] = Y
    
    size = int(np.max(M[:,1]) + 1)
    
    psi = make_psi_0(size)
    
    U = make_U(M, size, DT)
    psi_t = np.empty((size, int(TOTAL_TIME/DT)))
    
    psi_t[:,0] = psi
    
    for tt in range(int(TOTAL_TIME/DT-1)):
        psi = U.dot(psi)
        psi_t[:, tt+1] = psi
    
    import plot_electron_cascade as pec
    
    pec.plot_charge_prob(psi_t, TOTAL_TIME, DT, ES)
    
    pec.plot_distribution(psi, ES)
    
    return psi, ES, M
