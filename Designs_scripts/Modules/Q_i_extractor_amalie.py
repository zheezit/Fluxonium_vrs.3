#Based on the measurements using labber, we want to be able to extract the Q_i 
# (this is only a code for extracting the Q_i, not for calculating it)


# import lmfit
# import scipy.io as sio
import resonator
from resonator import background, shunt, see
# import random
# import matplotlib.patches as mpatches
import numpy as np
import matplotlib.pyplot as plt
# from numpy import loadtxt, savetxt
# from scipy.signal import find_peaks
import Labber

# Fancy plot font, can be removed if it causes any issue
# from matplotlib import font_manager
#font_path = '/Users/cfl831/Documents/Font/cmunrm.ttf'
# font_path = '/Users/cfl831/Documents/Font/arial.ttf'
# prop = font_manager.FontProperties(fname=font_path)
# fsize = 18

# filename_1 = r"C:\Users\T2-1\Dropbox\My PC (T2-1)\Desktop\Zhenhai\data_processing\generalCode\res4Quality.hdf5"
filename_1 =  r"C:\Users\jiaop\OneDrive\Skrivebord\Fluxonium\python\Modules\Res8_powerscan_10dB_2.hdf5"
filename = [filename_1]
Qi = []
Qi_err = []
Lfile = Labber.LogFile(filename[0])
# print(len(Lfile.getTraceXY(entry=1)[0]))
freq, _ = Lfile.getTraceXY(entry=2)
# print((freq))
S21 = Lfile.getData()
# print(S21[0])
print((S21)[0])
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


# plt.style.use("presentation.mplstyle")
plt.figure(figsize=(7, 5))
power = np.linspace(10, -60, np.shape(S21)[0])
Qi = np.array(Qi)
Qi_err = np.array(Qi_err)
print(Qi_err)
plt.errorbar(x=power, y=Qi/1e6, yerr=Qi_err/1e6, linestyle='', marker='o', ecolor='k', color='k', ms=5, linewidth = 1, elinewidth=1)
plt.ylabel("$Q_i$ (1e6)", fontsize=15)
plt.xlabel("VNA power ($dBm$)", fontsize=15)
plt.tight_layout
plt.show()


# frequency, S21 = freq, S21
# lsf = shunt.LinearShuntFitter(frequency=frequency, data=S21)
# print(lsf.result.fit_report())
# fig, axes = see.real_and_imaginary(resonator=lsf)
    