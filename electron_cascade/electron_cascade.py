# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:06:55 2020

@author: chels
"""

import numpy as np
import plot_electron_cascade as pec
from make_electronic_states import make_elec_states
import pickle


TOTAL_TIME = 2 #fs
DT = .0001 #fs

if True:
    ES, M = make_elec_states(True)
else:
    with open("electronic_states.pkl", "rb") as f:
        ES = pickle.load(f)
    with open("decay_pathway.pkl", "rb") as f:
        M = pickle.load(f)

size = int(np.max(M[:,1]) + 1)


M[list(range(19)),2] = .4/.3*19
M[[-1,-2], 2] = .4/.7*2
#M[21,2] = 10

def main():
    
    psi = make_psi_0()
    
    U = make_U(size, DT)
    psi_t = np.empty((size, int(TOTAL_TIME/DT)))
    
    for tt in range(int(TOTAL_TIME/DT)):
        psi = U.dot(psi)
        psi_t[:, tt] = psi
        
    print('The final probability distribution is: ')
    print(psi)
    
    #pec.plot_state_prob(psi_t, TOTAL_TIME, DT, ES)
    
    return psi


def coupling_term(i, j, coeff, size): #coeff in fs^-1
    
    delta_U = np.zeros((size, size))
    
    delta_U[i,i] = -coeff
    delta_U[j,i] = coeff
    
    return delta_U


def make_U(size, dt): #dt in fs
    
    U = np.eye(size)
    
    for line in M:

        U += coupling_term(int(line[0]), int(line[1]), dt/line[2]*line[3], size)
        #print(line[3])
        
    return U


def make_psi_0():
    psi = np.zeros((size))
    psi[0] = 1
    
    return psi
    

psi = main()

#if __name__ == '__main__':
#    main()