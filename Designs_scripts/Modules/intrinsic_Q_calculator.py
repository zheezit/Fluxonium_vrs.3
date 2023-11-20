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
us = 1e-6

def intrinsic_Q_calculator(w_10,w_r,T_1q,g,Q_lr): # you can find out if your intrinsic quality factor changes? 
    # We want to find the intrinsic Q_factor where we have substracted the purcell Q_factor
    
    N = len(T_1q)  # T_1 is an array
    print(N)
    g = np.full(N,g) # now g is also an array. g = coupling stregnth between qubit and resonator.   
    w_r = np.full(N, w_r) # w_r is the frequency of the resonator

    Q_q = w_10*T_1q # Q_q is the quality fator of the qubit it is found by multiplying w_10 and T_1q. The qubit quality factor is also called the external quality factor. 
    
    T_1pur = (Q_lr*(w_10-w_r)**2)/(w_r*g**2) 
    Q_pur = w_10*T_1pur
    
    Q_i = 1/((1/Q_q)-(1/Q_pur)) # The Q_i is the intrinsic quality factor = 
    return Q_q,Q_pur,Q_i, T_1pur




T_1q = np.array([7.685622091491206407e-07,8.441321992111699842e-07,4.767696826920999918e-07,6.957561378866380843e-07,5.053764863582287635e-07,4.218490306988432732e-07,3.675885714671787216e-07,6.208258841894463627e-07,6.819386673187718094e-07,6.505143120321203275e-07,7.524873248672124129e-07,6.291998120742497458e-07,5.245019668480554777e-07,7.196934937149299794e-07,9.825734371194028633e-07,6.950144361821310086e-07,9.084743849063010098e-07,9.652338855382528889e-07,1.157983297277515144e-06,1.199879192792310015e-06]) # in seconds
f_10 = np.array([4.653600000000000000e+09,4.784600000000000000e+09,4.920600000000000000e+09,4.877600000000000000e+09,4.768600000000000000e+09,4.746600000000000000e+09,4.610600000000000000e+09,4.514600000000000000e+09,4.499600000000000000e+09,4.474600000000000000e+09,4.291600000000000000e+09,4.085600000000000000e+09,4.020600000000000000e+09,3.992600000000000000e+09,4.130600000000000000e+09,4.037600000000000000e+09,3.875600000000000000e+09,4.086600000000000000e+09,4.085600000000000000e+09,3.891600000000000000e+09]) # in Hz
# f_10 = np.linspace(5.0*GHz,6.0*GHz,20) # in GHz

w_10 = f_10*2.0*np.pi
g = 50.0*MHz *2*np.pi
w_r = 6.34* GHz * 2*np.pi
Q_lr = 5000

Q_q,Q_pur,Q_i, T_1pur = intrinsic_Q_calculator(w_10,w_r,T_1q,g,Q_lr)
print(f"Q_pur=",Q_pur)
print(f"Q_q",Q_q)
print(f"Q_i=",Q_i)



# Here we plot the T_1 as a function of f_q where we take into account the purcell factor which occurs in the dispersive regime. 

fig, ax = plt.subplots(1,3,figsize=(12, 4))
ax[0].plot(f_10/GHz,1/Q_q, ".")
ax[0].set_title("1/Q_q")
ax[0].set_xlabel("f_10(GHz)")
ax[0].set_ylabel("Q_x")


ax[1].plot(f_10/GHz,1/Q_pur, ".")
ax[1].set_title("1/Q_pur")
ax[1].set_xlabel("f_10(GHz)")


ax[2].plot(f_10/GHz,Q_i , ".")
ax[2].set_xlabel("f_10(GHz)")
ax[2].set_title("Q_i intrinsic")

plt.show()