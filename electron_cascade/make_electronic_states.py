# -*- coding: utf-8 -*-
"""
Created on Thu May 21 14:58:20 2020

@author: chelsea
"""


def magnitude(x):
    import math
    return int(math.log10(x))




def make_elec_states(save):
        
    import numpy as np
    import pickle
    import time
    from sorting_estates import sortprocess
    
    
    
    tic = time.time()
    
    HBAR = 4.1
    
    M = np.loadtxt('Decay_Process.txt',comments='#')
    
    widths = M[0,1:]
    initial_state = M[1,1:]
    initial_excitation = M[2,1:]
    
    processes = M[3:,1:]
    
    processes, p_index = sortprocess(processes)
    
    electronic_states = np.empty((1,np.size(initial_state,0)))
    electronic_states[0,:] = initial_excitation

    e_index = 0
    for kk in range(np.size(initial_excitation)):
        e_index = e_index + 10**kk*abs(initial_excitation[-(kk+1)])
    e_index = np.array([e_index])
    
    ii = 0
    
    
    while ii < np.size(electronic_states, 0):
        num_process = sum((p_index >= 10**magnitude(e_index[ii])).astype(int))
        done_process = sum((p_index > 10**(magnitude(e_index[ii])+1)).astype(int))
        for jj in range(done_process, num_process):
            
            possible_state = electronic_states[ii,:] + processes[jj,:]
    
            if np.all(abs(possible_state) <= initial_state):
    
                electronic_states = np.vstack((electronic_states, possible_state))
                e_in = 0
                for kk in range(np.size(possible_state)):
                    e_in = e_in + 10**kk*abs(possible_state[-(kk+1)])
                    
                e_index = np.concatenate((e_index, np.array([e_in])))
                
                index1 = np.where(processes[jj,:]==1)
                num1 = initial_state[index1]+electronic_states[ii,index1]
                
                if np.any(processes[jj,:]<-1):

                    index2 = np.where(processes[jj,:]==-2)
                    num2 = initial_state[index2]+electronic_states[ii,index2]
                    mult = num1*num2*(num2-1)
                    if ii == 0 and jj == 0:
                        decay_pathway = np.array([ii, np.size(electronic_states,0)-1, HBAR/np.dot(widths,np.abs(processes[jj,:])), int(mult[0])])
                    else:
                        decay_pathway = np.vstack((decay_pathway, np.array([ii, np.size(electronic_states,0)-1, HBAR/np.dot(widths,np.abs(processes[jj,:])), int(mult[0])])))
                    
                else:
                    
                    index2 = np.where(processes[jj,:]==-1)
                    num2 = initial_state[index2]+electronic_states[ii,index2]
                    mult = num1*np.prod(num2)
                    if ii == 0 and jj == 0:
                        decay_pathway = np.array([ii, np.size(electronic_states,0)-1, HBAR/np.dot(widths,np.abs(processes[jj,:])), int(mult[0])])
                    else:
                        decay_pathway = np.vstack((decay_pathway, np.array([ii, np.size(electronic_states,0)-1, HBAR/np.dot(widths,np.abs(processes[jj,:])), int(mult[0])])))
                    
    
        ii += 1
            

    print('took ' + str(int(time.time()-tic)) + ' seconds')
    
    if save:
        with open("electronic_states.pkl", "wb") as f:
            pickle.dump(electronic_states, f)
            
        with open("decay_pathway.pkl", "wb") as f:
            pickle.dump(decay_pathway, f)


    return electronic_states, decay_pathway