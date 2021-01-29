# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 18:06:46 2021

@author: chelsea
"""

#molar_con in mM, set FeCN6_or_FeRu True for FeCN6 False for FeRu

def make_CXRO_input(molar_con, FeCN6_or_FeRu): 
    
    
    Fe_aw = 55.85 #g/mol
    H2O_aw = 18.02 #g/mol
    C_aw = 12.01 #g/mol
    N_aw = 14.01 #g/mol
    Ru_aw = 101.07 #g/mol    
    
    
    
    bg_formula = 'H2O'
    
    #           molar_con * 10^-3 mol | 1 Liter H2O   | 1 cm^3 H2O | H2O_aw
    #Fe_frac = -----------------------|---------------|------------|-----------
    #           1 Liter H20           | 1000 cm^3 H2O | 1 g H2O    | 1 mol H2O
    
    Fe_frac = molar_con*H2O_aw/10**6
    
    bg_formula += 'C{:.4f}'.format(Fe_frac*6)
    if FeCN6_or_FeRu:
        bg_formula += 'N{:.4f}'.format(Fe_frac*6)
        bg_density = 1 + molar_con*(C_aw+N_aw)/10**6
    else:
        bg_formula += 'N{:.4f}Ru{:.4f}'.format(Fe_frac*11,Fe_frac)
        bg_density = 1 + molar_con*(C_aw+N_aw+Ru_aw)/10**6
    
    
    
    
    
    
    
    
    
    Fe_formula = 'Fe'
    
    #              molar_con * 10^-3 mol | 1 Liter H2O   | Fe_aw
    #Fe_density = -----------------------|---------------|----------
    #              1 Liter H20           | 1000 cm^3 H2O | 1 mol Fe
    
    Fe_density = molar_con*Fe_aw/10**6


    return (bg_formula, bg_density, Fe_formula, Fe_density)
