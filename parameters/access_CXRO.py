# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 15:40:17 2021

@author: chelsea
"""


def get_spectrum(formula, density, thickness, min_eV, max_eV, n_steps):
    from selenium import webdriver
    
    driver = webdriver.Chrome()
    driver.get('https://henke.lbl.gov/optical_constants/filter2.html')
    
    formula_box = driver.find_element_by_name('Formula')
    formula_box.clear()
    formula_box.send_keys(formula)
    
    density_box = driver.find_element_by_name('Density')
    density_box.clear()
    density_box.send_keys(str(density))
    
    thickness_box = driver.find_element_by_name('Thickness')
    thickness_box.clear()
    thickness_box.send_keys(thickness)
    
    max_eV_box = driver.find_element_by_name('Max')
    max_eV_box.click()
    max_eV_box.send_keys(u'\ue003')
    max_eV_box.send_keys(u'\ue003')
    max_eV_box.send_keys(u'\ue003')
    max_eV_box.send_keys(u'\ue003')
    max_eV_box.send_keys(max_eV)
    
    min_eV_box = driver.find_element_by_name('Min')
    min_eV_box.click()
    min_eV_box.send_keys(u'\ue003')
    min_eV_box.send_keys(u'\ue003')
    min_eV_box.send_keys(min_eV)
    
    n_steps_box = driver.find_element_by_name('Npts')
    n_steps_box.clear()
    n_steps_box.send_keys(n_steps)
    
    submit_button = driver.find_element_by_xpath('/html/body/form/input')
    submit_button.click()
    
    chwd = driver.window_handles
    driver.switch_to.window(chwd[1])
    
    data_file_button = driver.find_element_by_xpath('/html/body/center/h2/a')
    data_file_button.click()
    
    data_loc = driver.find_element_by_xpath('/html/body')
    data = data_loc.text
    
    driver.close()
    driver.switch_to.window(chwd[0])
    driver.close()
    
    data = data.split('\n')
    
    info = data[0:2]
    
    data = data[2:]
    
    energy = [float(datum.split()[0]) for datum in data]
    spectrum = [float(datum.split()[1]) for datum in data]
    
    return (info, energy, spectrum)
