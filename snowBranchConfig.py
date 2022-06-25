import numpy as np
import os
# import snowBranchConfig as config
import lib.rtcOutput as rtOut
from LUT.interpScatMatr import interpScatProp as interp
import lib.scatteringFiles as scat
import lib.createInput as input
import time
import pandas as pd
import glob, os
import lib.scatteringFiles as scat
import re
import matplotlib.pyplot as plt


# Configuration file for the general 2-layer snow scene described on page 14 of project log:
# https://docs.google.com/document/d/1pSP3slZeSooPrD4k_ExOR3gl9Iy77iYiekMRwFCqz18/edit#heading=h.ub209o5ykrsf

rt_dir = "/home/accurt/rt_code/rt_code/"
data_dir = "/home/accurt/Data/"
# Dictionary of scattering files to interpolate on for each wavelength
scatt_dir_dict = {
    0.41027 : '/home/accurt/Downloads/ice_reff_410/',
    0.46913 : '/home/accurt/Downloads/ice_reff_469/',
    0.55496 : '/home/accurt/Downloads/ice_reff_555/',
    0.67001 : '/home/accurt/Downloads/ice_reff_670/',
    0.86351 : '/home/accurt/Downloads/ice_reff_865/',
    0.96 : '/home/accurt/Downloads/ice_reff_960/',
    1.58886 : '/home/accurt/Downloads/ice_reff_1589/',
    1.88 : '/home/accurt/Downloads/ice_reff_1880/',
    2.26438 : '/home/accurt/Downloads/ice_reff_2264/'
    }


lambda_names            = np.array(["410","470", "555", "670","870","960","1590","1880","2264"])
lambda_nm               = np.array([0.41027, 0.46913, 0.55496, 0.67001, 0.86351, 0.96, 1.58886, 1.88, 2.26438]) # actual floats value
lambda_colors_hex       = ["#FF33F3", "#3633FF", "#4EFF33", "#FF0000", "#FFDA00", "#800000", "#FF43A6", '#808080', "#000000"]
lambda_colors_str       = ["purple", "blue", "green", "red", "orange", "maroon", "magenta", "grey", "black"]

dataType = 1
# dataToModel = "RSP1-B200_L1C-RSPCOL-CollocatedRadiances_20100511T174714Z_V002-20210618T180640Z.h5"
dataToModel = "RSP1-B200_L1C-RSPCOL-CollocatedRadiances_20100511T191613Z_V002-20210618T180930Z.h5"
#### 0 means sythetic
#### 1 means RSP new format
#### 2 means RSP pace-like
#### 3 means HARP-2
#### 4 means RSP old format

# Switches for wavelenghts and polarization types
# 1 = on, 0 = off

switch_which_lambdas     = [0,1,0,0,1,0,0,0,0] #which_lambdas rename [1]
switch_I                 = [0,1,0,0,1,0,0,0,0] #include total reflectance? [1]
switch_polarization      = [0,1,0,0,1,0,0,0,0] #include polarization? [1]
switch_DoLP              = [0,1,0,0,1,0,0,0,0] #polarized reflectance = 0, dolp = 1 [1]
switch_oil_detection     = 0  # 0    means no restriction of Dolp based on cox and munch
                              # 1    means utilize cox and munk

# Wavelength names and values based on switches, NO NEED TO CHANGE
active_lambda_names = lambda_names[np.array(switch_which_lambdas) == 1]
active_lambda_colors = [lambda_colors_hex[i] for i in range(len(lambda_colors_hex)) if (switch_I[i] == 1 or switch_polarization[i] == 1 or switch_DoLP[i] == 1)]
ALAM = [lambda_nm[i] for i in range(len(lambda_nm)) if (switch_I[i] == 1 or switch_polarization[i] == 1 or switch_DoLP[i] == 1)]




MCAP, NCAP, NCAP2, NTAU, NTAU2, MTOT=50, 18, 18, 24, 24, 25
NTYPE = 4
N3BY3, QSTOP, QSTOP2, nPhi, nGauss, ERRBNDR, ERRBNDP=7, 1.000E-20, 1.000E-20, 256, 24, 2.000E-8, 1.000E-8
mu0, phi= 0.789254, 0.000000000
NTHETA=24
NEXTR=1
IGAUSS=2
ALBEDO = 0.00
SURFACE_FILENAME = ["srfNotNeededForSnow"]*(len(ALAM))*NTYPE
OUTPUT_FILENAME = [f"firstInv{name}" for name in active_lambda_names]
NPERS, NLAM, NLAYER, IPRT, IREMV = 2, (len(ALAM)), 3, 0, 1 #CHECK IF JUST 2 LAYERS OR INCLUDE ATMOSPHERE
A = [0.15000, 56.3, 71.4, 0.1] #, 0.7626] # layers in order here are soot, snow layer 1, snow layer 2, fine mode, coarse mode
B = [0.10000, 0.5,   0.7, 0.45] #, 0.672] # layers in order here are soot, snow layer 1, snow layer 2, fine mode, coarse mode

# Dictionary of fine mode aerosol refractive indices for different wavelengths

REFRAC_INDEX_DICT_FINE_MODE = {
    0.55496:(1.483000, 1.00E-02),
    0.41027:(1.503000, 1.00E-02),
    0.46913:(1.493000, 1.00E-02),
    0.67001:(1.473000, 1.00E-02),
    0.86351: (1.463000, 1.00E-02),
    1.58886: (1.443000, 1.00E-02),
    2.26438: (1.423000, 1.00E-02)
}

# Dictionary of coarse mode refractive indices for different wavelengths

REFRAC_INDEX_DICT_COARSE_MODE = {
    0.55496:(1.333000 , 0.00E-03),
    0.41027:(1.338600, 0.00E-02),
    0.46913:(1.336200, 0.00E-02),
    0.67001:(1.331000, 0.00E-02),
    0.86351: (1.327500, 3.55E-07),
    1.58886: (1.318200, 1.04E-04 ),
    2.26438: (1.287500, 4.19E-04)
}

# Collects the correct refractive indices for the active wavelengths into a list of lists and flattens it
# I can explain this line if it is especially confusing
NR = [item for sublist in [[1.400000, 1.0, 1.0, REFRAC_INDEX_DICT_FINE_MODE[wl][0], REFRAC_INDEX_DICT_COARSE_MODE[wl][0]] for wl in ALAM] for item in sublist]
NI = [item for sublist in [[0.000E-2, 0.0, 0.0, REFRAC_INDEX_DICT_FINE_MODE[wl][1], REFRAC_INDEX_DICT_COARSE_MODE[wl][1]] for wl in ALAM] for item in sublist]

R1 = [0.0] * NTYPE
R2 = [10.0] * NTYPE
NSD = [3, 6, 6, 3] * len(ALAM)
SCATTERING_FILENAME = ["A70B09L2262.mie", "placeholderFile", "placeholderFile", "A70B09L2262.mie"]* len(ALAM) #, "A70B09L2262.mie"]  #scattering_filename rename ["A70B09L2262.mie", "A70B09L2262.mie"]
DELP = [0.12524524826760172, 0.003833820025465684, 1017.8709209317069]
TAUREP = 1

# Order of species here is soot, snow layer 1, snow layer 2, fine mode aersol, coarse mode aerosol
SPECIES_AMOUNT =  [[0.00E-02, 0.00E-01,  0.00E-01],
                   [1.00E-01, 0.00E-01,  0.00E-01],
                   [0.00E-02, 3.00E-01,  0.00E-01],
                   [0.00E-02, 4.00E-01,  0.00E-01]] #,
                   #[0.00E-02, 5.00E-01,  0.00E-01]] #species_amount rename
NGAS = 0
TAUABS = []


# Dictionary of SNOW refractive indices for different wavelengths

REFRAC_INDEX_DICT = {
    #  WAVELENGTH  :  (NR, NI)
    0.41027    :  (1.31850, 2.66900e-11),
    0.46913    :  (1.31456, 1.89290e-10),
    0.55496    :  (1.31080, 2.56400e-09),
    0.67001    :  (1.30760, 1.89000e-08),
    0.86351    : (1.30382, 2.35000e-07),
    0.962    :  (1.30216,  7.89201e-07),
    1.58886   :  (1.28965, 0.000307069),
    1.8840   :   (1.27907, 0.000228580),
    2.2117   :   (1.26858,  0.000646712)
    }


# List of values for aspect ratio, roughness, and mixing proportion for the two-layer snow scene
arArr = [0.356, 0.356]
dArr = [0.5, 0.5]
fArr = [0.25, 0.25]

mu = 0.046 # mu of impurity
sigma = 1.5 # sigma of impurity
# f_imp = 1.0  # ppmw
rho_snow = 0.1 # g/cm^3
rho_imp  = 1.8 # g/cm^3
# wl       = 0.86351 # micron

# CHANGE TO A DICTIONARY BASED ON WAVELENGTH
nr_imp   = 1.85 #
ni_imp   = 0.71 #
# thickness = 0.98 # meters
soot = [0.75, 100.0]
dep_2 = 0.98 #meters
dep_1 = 0.02



def prepare_snow_iop(ar, d, reff, f_col, wl):
    ## interpolate and mix to get the snow IOP
    # ar: aspect ratio for columns
    # d: roughness parameter
    # reff: effective radius in microns
    # f_col: the fraction of columns in the mixture


    # Retrieve the appropriate directory of scattering files for the passed wavlength
    scatt_dir = scatt_dir_dict[wl]
    # interpolate to get the IOP for columns
    interpolant_1 = [ar, d, reff]
    c = interp(scatt_dir, wl, interpolant_1)
    ssc_prop_interp_arr_col, scattering_matrix_interp_arr_col = c.interp_NDLinear()

    # interpolate to get the IOP for plates
    interpolant_2 = [1. / ar, d, reff]
    c = interp(scatt_dir, wl, interpolant_2)
    ssc_prop_interp_arr_pla, scattering_matrix_interp_arr_pla = c.interp_NDLinear()

    # mix the IOPs with given f_col
    ssc_prop_arr = f_col * np.array(ssc_prop_interp_arr_col) + \
                   (1. - f_col) * np.array(ssc_prop_interp_arr_pla)
    ssc_prop_arr = list(ssc_prop_arr)

    scattering_matrix_arr = []
    for i in range(len(scattering_matrix_interp_arr_col)):
        scattering_matrix_element = f_col * scattering_matrix_interp_arr_col[i] + \
                                    (1. - f_col) * scattering_matrix_interp_arr_pla[i]
        scattering_matrix_arr.append(scattering_matrix_element)

    scatt_angles = c.scatt_angles

    return ssc_prop_arr, scatt_angles, scattering_matrix_arr





if __name__ == "__main__":
    # This checks that the config variables are setup correctly to generate a working .info file of a snow scene 
    test_file = input.Atmo(MCAP, NCAP, NCAP2, MTOT, N3BY3, QSTOP, QSTOP2, ERRBNDR, ERRBNDP, IGAUSS, IPRT,
                            IREMV, R1, R2, ALBEDO, SURFACE_FILENAME, OUTPUT_FILENAME, SCATTERING_FILENAME, NTAU, NTAU2, nPhi,
                                nGauss, NPERS, NTYPE, NLAM, NLAYER, NGAS, A, B, NSD, mu0,
                                    phi, ALAM, NR, NI, SPECIES_AMOUNT, TAUABS, DELP)
    test_file.createAtmo(totalName = "/home/accurt/Documents/test_info_inversion.info")
    
    quit()
