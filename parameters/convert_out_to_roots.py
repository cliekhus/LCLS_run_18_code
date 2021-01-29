# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

def extract_energy(file_name):

    import numpy as np
    
    f = open(file_name)
    content = f.read().split('Root')
    content = content[1:]
    
    energy = []
    strength = []
    
    for line in content:
        try:
                
            energy = energy + [float(line.split()[4])]
            strength = strength + [float(line.split()[44])]
        
        except:
            
            energy = energy + [float(line.split()[5])]
            strength = strength + [float(line.split()[45])]
        
    f.close()
        
    return np.array(energy), np.array(strength)
