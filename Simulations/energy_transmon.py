#Weak 2 excersise 1 
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
# np.set_printoptions(threshold=sys.maxsize)


save_plots = False
colors = plt.cm.Set3(np.linspace(0.3, 1.1, 8)) 




def hamiltonian(E_J1,E_J2,E_C,phi_e,N, phi_max):
    gamma = E_J2/E_J1
    d = (gamma-1)/(gamma+1)
    E_J = (E_J1+E_J2)*np.sqrt(math.cos(phi_e)**2 +d**2* (math.sin(phi_e)**2)) # a new Josephson energy
    # e = 1.60217663*10**(-19) # electron charge in coulombs
    e = 1

    # # make our matrix phi
    Phi = np.zeros((N,N))
    delta = 2*abs(phi_max)/(N-1)
    print(delta)
    for i in range(N):
        Phi[i][i]= -abs(phi_max)+delta*i
    print(Phi)

    # # make our matrix q 
    # set hbar to 1
    a = np.ones((1, N-1))[0]
    # print(np.diag(-a, -1) + np.diag(a, 1))
    q = np.dot((np.diag(-a, -1) + np.diag(a, 1)), (-(1j))/(2*delta))

    # # q^2 approximated: 
    a = np.ones((1, N-1))[0]
    b = np.ones((1,N))[0]
    # print(( np.diag(-2*b,0) + np.diag(a, -1) + np.diag(a, 1)))
    q_2 = np.dot(( np.diag(-2*b,0) + np.diag(a, -1) + np.diag(a, 1)), (-(1))/(delta**2))

    # # josephson junction
    JJ = np.zeros((N,N))
    for i in range(N):
        JJ[i][i] = E_J*np.cos(Phi[i][i])
    Hamiltonian = np.dot(4*E_C*np.square(1/(2*e)),q_2) - JJ

    return Hamiltonian, E_J

E_J1 = 2
E_J2 = 1
E_C = 1
phi_e = np.pi
phi_max = 2*np.pi
N = 100+1
# hamiltonian(E_J1,E_J2,E_C,phi_e,N, phi_max)
Hamiltonian, E_J = hamiltonian(E_J1,E_J2,E_C,phi_e,N, phi_max)

print(Hamiltonian)

eig_vals, eig_vec = sp.linalg.eigh(Hamiltonian)
print(eig_vals)

print(eig_vals[0])
print(eig_vec.T[0])

# idx = eig_vals.argsort()[::-1]   
# eigenValues = eig_vals[idx]
# eigenVectors = eig_vec[:,idx]

# print(f"eigenvalues",eig_vals)

# print(f"eigenvectors",eig_vec)
# print(eig_vec)

# # plot the potential as a function of the psi
# Generate N numbers between -pi and pi
x = np.linspace(-np.pi, np.pi, N)

# The potential equation
y =-E_J*np.cos(x)

# Eigenstates does not have any unit - therefore we add the eigenenergies
# we also plot the eigenstate squared becuase thet it the probability distribution. 
plt.plot(x, y)

for i in range(4):
    plt.plot (x, 4*abs(eig_vec.T[i])**2+eig_vals[i])
plt.show()

# # ----------------------------------------- Problem E2 - Plot the noise ------------------------------- #






