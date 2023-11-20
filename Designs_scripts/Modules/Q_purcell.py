import numpy as np 
from numpy import linalg as LA
import scipy as sp 
from scipy import sparse
from scipy.sparse import linalg

import sys
import math as math
import matplotlib 

from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib.widgets import Slider, Button
matplotlib.use('TkAgg')
GHz, MHz = 1e9, 1e6
us = 1e6

# np.set_printoptions(threshold=sys.maxsize)
w_10 = np.linspace(2*np.pi*4.25*GHz,2*np.pi*6.2*GHz,100) # in GHz
fig, ax = plt.subplots(1,3,figsize=(12, 4))
# h = 6.62*10**(-34) 



# here we plot the T_1 as a function of qubit frequency

Q_i = 0.5*10**6
# Q_i = 4.8 * GHz *2*np.pi * 0.6 *1e-6
T_1i = Q_i/(w_10)*us
line, = ax[0].plot(w_10/(2*np.pi*GHz), T_1i)
ax[0].set_xlabel("f_10(GHz)")
ax[0].set_ylabel("T_1 (us)")
ax[0].set_title("T_1 intrinsic")

# Here we plot the T_1 as a function of f_q where we take into account the purcell factor which occurs in the dispersive regime. 
Q_l = 6000
w_r = 2*np.pi*6.3*GHz # GHz
g = 0.05*(2*np.pi)*GHz # GHz -  50 MHz 
E_c = 200
T_1_purcell =((w_10-w_r)**2*Q_l)/(g**2*w_r)
line, = ax[1].plot(w_10/(2*np.pi*GHz),T_1_purcell*us)
ax[1].set_title("T_1 purcell effect")
ax[1].set_xlabel("f_10(GHz)")

# ((3-w_r)**2*Q_i)/(g**3)


# this is the overall T_1

Q_pur = 2*np.pi*w_10/(2*np.pi)*T_1_purcell

Q_q = 1/(1.0/Q_i+1.0/Q_pur)

T_1 = Q_q/(w_10)*us
ax[2].plot(w_10/(2*np.pi*GHz),T_1)
ax[2].set_title("T_1 overall")


plt.show()

