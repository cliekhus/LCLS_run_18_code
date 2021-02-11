# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 17:29:48 2020
@author: chelsea
"""

def load_data(bg_energy, bg_spectrum, Fe_energy, Fe_spectrum):
    
    import numpy as np
    import h5py
    
    FeCN6_file = 'FeCN6.csv'
    FeCN6_edge_file = 'FeCN6edge.csv'
    
    
    background = np.stack((np.array(bg_energy), np.array( bg_spectrum)), axis=1)
    
    Fe_edge = np.stack((np.array(Fe_energy), np.array(Fe_spectrum)), axis=1)
    
    
    FeCN6_edge = np.loadtxt(FeCN6_edge_file, delimiter=', ')
    FeCN6_edge = FeCN6_edge[FeCN6_edge[:,0].argsort()]
    
    FeCN6_paper = np.loadtxt(FeCN6_file, delimiter=', ')
    FeCN6_paper = FeCN6_paper[FeCN6_paper[:,0].argsort()]

    APSName = h5py.File('APS_Aug_2015_Fesamples.mat', mode = 'r')
    FeII = np.array(APSName['/FeII_ref_RIXS'])
    incident_axis = 1000*np.array(APSName['/Fe_RIXS_incident_axis'])
    
    FeII_XANES = np.sum(FeII, axis = 1)
    
    FeCN6_APS = np.transpose(np.vstack((incident_axis[:,0], FeII_XANES)))
    
    return (background, FeCN6_edge, Fe_edge, FeCN6_paper, FeCN6_APS)



def scale_factors(mol_paper, mol_edge_paper, atom_edge, mol_APS):
    
    import numpy as np
    from scipy.interpolate import interp1d
    
    f = interp1d(mol_edge_paper[:,0], mol_edge_paper[:,1], kind='cubic')
    peaks = mol_paper[:,1] - f(mol_paper[:,0])
    B_amp_paper = peaks[np.argmax(peaks[0:13])]
    B_energy_paper = mol_paper[np.argmax(peaks[0:13]),0]
    
    
    atom_edge = 1-atom_edge[:,1]
    edge_amp = (max(atom_edge)-min(atom_edge))
    
    
    f = interp1d(np.append(mol_APS[0:29,0], np.append(mol_APS[49,0], mol_APS[64:-1,0])), 
                 np.append(mol_APS[0:29,1], np.append(mol_APS[49,1], mol_APS[64:-1,1])), 
                 kind = 'cubic', fill_value="extrapolate")
    peaks = mol_APS[:,1] - f(mol_APS[:,0])
    B_amp_APS = peaks[49+np.argmax(peaks[49:-1])]
    B_energy_APS = mol_APS[49+np.argmax(peaks[49:-1]),0]
    
    return (B_amp_paper, B_energy_paper, edge_amp, min(atom_edge), B_amp_APS, B_energy_APS)



def ratio(cascade_ratios, excitation_fraction):
    
    excitation_ratio = cascade_ratios * excitation_fraction
    
    excitation_ratio[0] = 1-sum(excitation_ratio)
    
    return excitation_ratio



def broaden_spectrum(WIDTH, x_axis, energy, strength, num_roots):
    
    import numpy as np
    
    spectrum = np.zeros(np.shape(x_axis))
    
    for e, s in zip(energy[0:num_roots], strength[0:num_roots]):

        spectrum = spectrum + s*np.exp(-(x_axis-e)**2/WIDTH/2**.5)/2**.5
        
    return spectrum


def broaden_spectrum_no_signal(WIDTH, x_axis, energy, strength, num_roots, A_root):
    
    import numpy as np
    
    spectrum = np.zeros(np.shape(x_axis))
    
    for e, s in zip(energy[A_root:num_roots], strength[A_root:num_roots]):

        spectrum = spectrum + s*np.exp(-(x_axis-e)**2/WIDTH/2**.5)/2**.5
        
    return spectrum



def initial_shift(filename, B_peak_energy, WIDTH):
    
    import numpy as np
    from convert_out_to_roots import extract_energy
    
    energy, strength = extract_energy(filename)

    x_axis = np.linspace(min(energy)-10, 6971, 10000)
    
    spectrum = broaden_spectrum(WIDTH, x_axis, energy, strength, -1)

    calc_B = x_axis[np.argmax(spectrum)]
    
    return B_peak_energy - calc_B


def get_B_peak(spectrum, x_axis):
    
    from scipy.signal import find_peaks
    
    peaks_pos = find_peaks(spectrum, height=2e-6)
    
    B_energy = x_axis[peaks_pos[0][-2]]
    B_amp = spectrum[peaks_pos[0][-2]]
    
    return (B_energy, B_amp)


def excited_shift(initial_B, spectrum, x_axis):

    current_B, B_amp = get_B_peak(spectrum, x_axis)

    return current_B - initial_B


def generate_APS_edge(mol_APS, x_axis):
    
    import numpy as np
    
    from scipy.interpolate import interp1d
    from scipy.signal import savgol_filter
    
    f = interp1d(np.append(mol_APS[0:29,0], np.append(mol_APS[49,0], mol_APS[64:-1,0])), 
             np.append(mol_APS[0:29,1], np.append(mol_APS[49,1], mol_APS[64:-1,1])), 
             kind = 'cubic', fill_value='extrapolate')
    
    edge = f(x_axis) - f(x_axis[0])
    edge = savgol_filter(edge, 9, 3)
    
    return edge


def create_edge(B_shift, edge, x_axis):
    
    from scipy.interpolate import interp1d
   
    f = interp1d(x_axis + B_shift, edge, kind='linear', fill_value="extrapolate")
    
    return f(x_axis)
    



def create_signal(bg_energy, bg_spectrum, Fe_energy, Fe_spectrum, excitation_fraction):
    
    import numpy as np
    from convert_out_to_roots import extract_energy
    
    WIDTH = 1.5
    
    background, FeCN6_edge, Fe_edge, FeCN6_paper, FeCN6_APS = load_data(bg_energy, bg_spectrum, Fe_energy, Fe_spectrum)
    
    B_amp_paper, B_energy_paper, edge_amp, edge_zero, B_amp_APS, B_energy_APS = scale_factors(FeCN6_paper, FeCN6_edge, Fe_edge, FeCN6_APS)
   
    filenames = ['run-3p6_3d6-xanes.out', 'run-3p6_3d4-xanes.out']
    num_roots = [48, 50]
    A_roots = [0, 2]
    
    cascade_ratios = np.array([0, .1])
    ratios = ratio(cascade_ratios, excitation_fraction)
    
    shift = initial_shift(filenames[0], B_energy_APS, WIDTH) #This should be about 144.80 eV
    
    edge_APS = generate_APS_edge(FeCN6_APS, background[:,0])
    edge_APS = edge_APS / B_amp_APS * B_amp_paper
    
    spectra = np.empty((np.shape(background[:,0])[0], len(filenames)))
    spectra_no_signal = np.empty((np.shape(background[:,0])[0], len(filenames)))
    
    for ii, filename in enumerate(filenames):
        
        energy, strength = extract_energy(filename)
        energy = energy + shift
        
        spectrum = broaden_spectrum(WIDTH, background[:,0], energy, strength, num_roots[ii])
        spectrum_no_signal = broaden_spectrum_no_signal(WIDTH, background[:,0], energy, strength, num_roots[ii], A_roots[ii])
            
        if ii == 0:
            B_energy, B_amp = get_B_peak(spectrum, background[:,0])
            amp_scale = B_amp_paper/B_amp
        
        B_shift = excited_shift(B_energy_APS, spectrum, background[:,0])
        shifted_edge = create_edge(B_shift, edge_APS, background[:,0])
    
        spectrum = (spectrum*amp_scale + shifted_edge) * edge_amp + edge_zero + (1-background[:,1])
        spectrum_no_signal = (spectrum_no_signal*amp_scale + shifted_edge) * edge_amp + edge_zero + (1-background[:,1])
        
        spectra[:,ii] =  spectrum
        
        if ii == 0:
            spectra_no_signal[:,ii] = spectrum
        else:
            spectra_no_signal[:,ii] = spectrum_no_signal
    
    pumped = np.sum(ratios*spectra, 1)
    pumped_no_signal = np.sum(ratios*spectra_no_signal, 1)
    unpumped = spectra[:,0]
    
    return (background[:,0], pumped, pumped_no_signal, unpumped)