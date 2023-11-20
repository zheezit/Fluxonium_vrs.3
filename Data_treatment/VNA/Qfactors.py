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
# import Labber
import h5py as Labber

import os
import glob


# Fancy plot font, can be removed if it causes any issue
from matplotlib import font_manager
#font_path = '/Users/cfl831/Documents/Font/cmunrm.ttf'
font_path = '/Users/cfl831/Documents/Font/arial.ttf'
prop = font_manager.FontProperties(fname=font_path)
fsize = 18

#Fitting functions for the resonator peaks is found in the package "resonators"


# Specify the folder path
folder_path = r"N:\SCI-NBI-QDev\Amalie\Resonators\Chip_5_Resonator5\Data_treatment"

# Use glob to get a list of filenames in the folder
# You can specify a pattern to filter specific files, like "*.hdf5" for HDF5 filese
file_pattern = "*.hdf5"
filenames = glob.glob(os.path.join(folder_path, file_pattern))

# Now, 'filenames' is a list of all HDF5 files in the specified folder
filename = [filenames]
filename_name = glob.glob(os.path.join(folder_path, file_pattern))

# Extract file names from the paths and store them in a list
file_names_only = [os.path.basename(file) for file in filenames]

# Now, 'file_names_only' is a list of file names without the full path
# You can use this list in your header or any other part of your code
for file_name in file_names_only:
    print("Processing file:", file_name)



# filename_1 = r"C:\Users\T2-1\Dropbox\My PC (T2-1)\Desktop\Zhenhai\data_processing\generalCode\res4Quality.hdf5"
filename_1 =  r"N:\SCI-NBI-QDev\Amalie\Resonators\Chip_5_Resonator5\Data_treatment\Powerscan_res6_30dB.hdf5"
filename = [filename_1]
Qi = []
Qi_err = []
Lfile = Labber.LogFile(filename[0])
freq, _ = Lfile.getTraceXY(entry=2)
S21 = Lfile.getData()
for i in range(np.shape(S21)[0]):
    r = shunt.LinearShuntFitter(frequency=freq, 
                                data=S21[i, :],
                                background_model=background.MagnitudeSlopeOffsetPhaseDelay())
    Qi.append(r.Q_i) if r.Q_i_error is not None and r.Q_i_error < r.Q_i else  Qi.append(np.nan)
    Qi_err.append(r.Q_i_error) if r.Q_i_error is not None and r.Q_i_error < r.Q_i else Qi_err.append(np.nan)
    # plt.figure()
    # fig, (ax_mag, ax_phase, ax_complex) = plt.subplots(1, 3, figsize=(13, 4), dpi=300)
    # see.magnitude_vs_frequency(resonator=r, axes=ax_mag, normalize=True, frequency_scale=1e-9)
    # see.phase_vs_frequency(resonator=r, axes=ax_phase, normalize=True, frequency_scale=1e-9)
    # see.real_and_imaginary(resonator=r, axes=ax_complex, normalize=True)
    
#plt.style.use("presentation.mplstyle")
plt.figure(figsize=(7, 5))
power = np.linspace(10, -60, np.shape(S21)[0])
Qi = np.array(Qi)
Qi_err = np.array(Qi_err)
print(Qi_err)
plt.errorbar(x=power, y=Qi/1e6, yerr=Qi_err/1e6, linestyle='', marker='o', ecolor='k', color='k', ms=5, linewidth = 1, elinewidth=1)
plt.ylabel("$Q_i$ (1e6)", fontsize=15)
plt.xlabel("VNA power ($dBm$)", fontsize=15)
# plt.ylim((0, 2))
# plt.yticks(ticks = np.linspace(0.6, 1.2, 4), label = np.linspace(0.6, 1.2, 4), fontsize=15)
plt.xticks(fontsize=15)
plt.grid(None)
plt.show()


# print(f"freq = {freq}")
# print(f"S21 = {S21}")
