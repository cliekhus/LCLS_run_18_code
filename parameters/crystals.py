# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 12:10:00 2021

@author: chelsea
"""





def calc_div_pixel_resolution(crystal_type, min_eV, max_eV):

    import math
    
    EV_TO_NM = 1239.8
    
    #divergence = 0.003/1.3/2
    dist_sample_crystal = 1.6 #m
    dist_crystal_detector = 2 #m
    pixel_size = 100 #microns
    
    central_wl = EV_TO_NM*2/(min_eV+max_eV)
    #central_wl = 0.17425158
    min_wl = EV_TO_NM/max_eV
    max_wl = EV_TO_NM/min_eV
    
    
    if crystal_type == 111:
        crystal_2d = 0.62712 #nm
        
    elif crystal_type == 220:
        crystal_2d = 0.384031 #nm
        
    elif crystal_type == 311:
        crystal_2d = 0.32750274 #nm
        
    theta_bragg_center = math.asin(central_wl/crystal_2d)
    theta_bragg_min = math.asin(min_wl/crystal_2d)
    theta_bragg_max = math.asin(max_wl/crystal_2d)
    
    offset_min = theta_bragg_min - theta_bragg_center
    offset_max = theta_bragg_max - theta_bragg_center
    
    offset_at_det_min = dist_sample_crystal*math.tan(offset_min) + \
                        dist_crystal_detector*(math.sin(2*theta_bragg_min+offset_min)-math.sin(2*theta_bragg_center))
                        
    offset_at_det_max = dist_sample_crystal*math.tan(offset_max) + \
                        dist_crystal_detector*(math.sin(2*theta_bragg_max+offset_max)-math.sin(2*theta_bragg_center))
                        
    sep_at_det_m = (offset_at_det_max - offset_at_det_min)*1e6 #um
    sep_at_det_pix = sep_at_det_m/pixel_size
    
    pixel_resolution = (max_eV-min_eV)/sep_at_det_pix
    
    return pixel_resolution

