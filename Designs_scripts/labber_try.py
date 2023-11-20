import scipy
import numpy as np
import matplotlib as plt
from scipy.signal import find_peaks

# first you have to make a path to the correct directory
import Labber 
import qiskit_metal

# Labber.LogFile(r"C:\Users\jiaop\OneDrive\Skrivebord\Fluxonium\Fabrication\Resonators\Res_chip5\measurements\Res6_powerscan_10dB.hdf5")

# filename_1 = r"C:\Users\jiaop\OneDrive\Skrivebord\Fluxonium\Fabrication\Resonators\Res_chip5\measurements\Res6_powerscan_10dB.hdf5"
# filename = [filename_1]
# Qi = []
# Lfile = Labber.LogFile(filename[0])
# freq, _ = Lfile.getTraceXY(entry=2)
# S21 = Lfile.getData()
# for i in range(np.shape(S21)[0]):
#     r = shunt.LinearShuntFitter(frequency=freq, 
#                                 data=S21[i, :],
#                                 background_model=background.MagnitudeSlopeOffsetPhaseDelay())
#     Qi.append(r.Q_i)
#     # plt.figure()
#     # fig, (ax_mag, ax_phase, ax_complex) = plt.subplots(1, 3, figsize=(13, 4), dpi=300)
#     # see.magnitude_vs_frequency(resonator=r, axes=ax_mag, normalize=True, frequency_scale=1e-9)
#     # see.phase_vs_frequency(resonator=r, axes=ax_phase, normalize=True, frequency_scale=1e-9)
#     # see.real_and_imaginary(resonator=r, axes=ax_complex, normalize=True)
    
# plt.style.use("presentation.mplstyle")
# plt.figure(figsize=(7, 5))
# power = np.linspace(10, -60, np.shape(S21)[0])
# Qi = np.array(Qi)

# plt.plot(power, Qi*1e-6, 'o', color = 'C0', markersize = 6, linewidth = 10)
# plt.ylabel("$Q_i$ (1e6)", fontsize=15)
# plt.xlabel("VNA power ($dBm$)", fontsize=15)
# plt.ylim((0, 2))
# # plt.yticks(ticks = np.linspace(0.6, 1.2, 4), label = np.linspace(0.6, 1.2, 4), fontsize=15)
# plt.xticks(fontsize=15)
# plt.grid(None)

# plt.legend(frameon=False,fontsize=15)

# plt.figure()
# fig, (ax_mag, ax_phase, ax_complex) = plt.subplots(1, 3, figsize=(13, 4), dpi=300)
# see.magnitude_vs_frequency(resonator=r, axes=ax_mag, normalize=True, frequency_scale=1e-9)
# see.phase_vs_frequency(resonator=r, axes=ax_phase, normalize=True, frequency_scale=1e-9)
# see.real_and_imaginary(resonator=r, axes=ax_complex, normalize=True)
# plt.savefig("Ta_resonator_Qi.pdf", format="pdf", bbox_inches="tight", transparent=True)
# plt.show()

