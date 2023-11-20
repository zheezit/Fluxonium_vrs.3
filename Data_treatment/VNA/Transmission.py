# import lmfit
import scipy.io as sio
import resonator
from resonator import background, shunt, see
import matplotlib.patches as mpatches
import numpy as np
import matplotlib.pyplot as plt
from numpy import loadtxt, savetxt
from scipy.signal import find_peaks
#read the hdf5 files from labber
import Labber

import os
import glob
hbar = 1.05457182*10**(-34) # m2*kg/ s


# we want to caluclate the photon number using the formula
P_VNA = -50
RT_attenuators = 20 # All in dB or dBm
Q_r =
Q_c =
w_0 =

def n_average(P_VNA, RT_attenuators, P_Michaela, Q_r, Q_c, w_0):
    P_in = P_VNA - RT_attenuators - P_Michaela
    n_average = 2/(hbar*w_0**2) * (Q_r**2)/Q_c  *P_in
    return n_average

