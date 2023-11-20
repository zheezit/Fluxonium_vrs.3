import numpy as np 
from numpy import linalg as LA
import scipy as sp 
from scipy import sparse
from scipy.sparse import csr_matrix
from scipy.sparse import lil_matrix
from scipy.sparse import linalg
from scipy import stats as stats
from scipy.integrate import solve_ivp, trapz
# from scipy.sparse.linalg import spmatrix_power

import sys
import math as math
import matplotlib 

from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib.widgets import Slider, Button
matplotlib.use('TkAgg')

save_plots = False
show_plots = True
colors = plt.cm.Set3(np.linspace(0.3, 1.1, 8)) 

import numpy as np
from scipy.constants import hbar

# class TransmonHamiltonian:
#     def __init__(self, E_J, E_C, N):
#         self.E_J = E_J # Josephson energy
#         self.E_C = E_C # charging energy
#         self.N = N     # number of charge states to include
        
#         # basis states
#         self.basis = np.identity(self.N)
        
#         # charge operator
#         self.n = np.diag(np.arange(self.N))
        
#         # Hamiltonian
#         self.H = 4 * self.E_C * (self.n - self.N/2 + 0.5)**2 - self.E_J * (np.diag(np.cos(np.arange(self.N-1) * np.pi / self.N)), 1) - self.E_J * (np.diag(np.cos(np.arange(self.N-1) * np.pi /


class transmon_charge:
    def __init__(self, E_J1, E_J2,E_C,phi_e,k, n_cutoff,n_g):
        self.E_J = E_J
        self.E_J1 = E_J1
        self.E_J2 = E_J2
        self.E_C = E_C
        self.phi_e = phi_e
        self.k = k
        self.n_cutoff = n_cutoff
        self.n_g = n_g
        
    # We make our phi matrix
    phi = sp.sparse.csr_matrix((k,k))
    phi.setdiag(1, k= -1)

    # We define our n-matrix with cutoff. 
    n_array = np.linspace(-n_cutoff,n_cutoff, k)
    n = sp.sparse.csr_matrix((k, k))
    n.setdiag(n_array)
    #we define our n2 matrix
    n2 = n @ n

    # we define our charge offset matrix
    n_g_array = np.linspace(-n_g,n_g, k)
    n_g = sp.sparse.csr_matrix((k, k))
    n_g.setdiag(n_g_array)

    # we define our phi matrix
    phi_inv = sp.sparse.csr_matrix((k,k))
    phi_inv.setdiag(1, k= 1)

    # we define our cos term
    cos = phi + phi_inv

    # calculate the capacitor term
    n_hat = n2 - 2*n_g
    Capacitor = n_hat*(4*E_C)

    # Calculate the Josephson term
    gamma = E_J2/E_J1
    d = (gamma-1)/(gamma)
    E_J = (E_J1+E_J2)*np.sqrt(math.cos(phi_e)**2 +d**2* (math.sin(phi_e)**2)) # a new Josephson energy
    
    JJ = cos.multiply(E_J)

    def Hamiltonian(self): 
        return Capacitor - JJ

    eig_vals, eig_vec = sp.linalg.eigh(Hamiltonian)

    w_q = eig_vals[1]-eig_vals[0]
    
    return eig_vals, eig_vec, Hamiltonian, n.toarray(), E_J, E_C


eig_vals, eig_vec, Hamiltonian, n, E_J, E_C = transmon_charge(E_J1,E_J2,E_C,phi_e,N, n_cutoff,charge_offset)

# print(Hamiltonian)
print(f"this is n: {n}")


# --------------------------------Hamiltonian of the transmon in the flux basis-----------------
def transmon_flux(E_J1,E_J2,E_C,phi_e,N, phi_cutoff,charge_offset):
    # We make our phi matrix
    phi_array = np.linspace(-phi_cutoff, phi_cutoff, N+1)
    phi_matrix = sp.sparse.csr_matrix((N+1, N+1))
    phi_matrix.setdiag(phi_array)
    # our delta
    delta = phi_array[2]-phi_array[1]
    # We make our n^2 matrix
    n2_matrix = sp.sparse.csr_matrix((N+1,N+1))
    n2_matrix.setdiag(-2)
    n2_matrix.setdiag(1,k=-1)
    n2_matrix.setdiag(1,k=1)
    n2_matrix[0,N] = 1
    n2_matrix[N,0] = 1
    n2_matrix = n2_matrix.multiply((-1)/(delta**2))

    # Make a matrix with the chargeoffset in the diagonal
    n_chargeoffset = sp.sparse.csr_matrix((N+1,N+1))
    n_chargeoffset.setdiag(charge_offset)

    # Make the n matrix
    n_matrix = sp.sparse.csr_matrix((N+1,N+1))
    n_matrix.setdiag(1,k=1)
    n_matrix.setdiag(-1,k=-1)
    n_matrix[0,N] = -1
    n_matrix[N,0] = 1
    n_matrix = n_matrix.multiply((-1j)/(2*delta))

    # calculate the capacitor term
    n = 2*n_chargeoffset*n_matrix
    Capacitor = (n2_matrix-n).multiply(4*E_C)

    # Calculate the Josephson term
    gamma = E_J2/E_J1
    d = (gamma-1)/(gamma+1)
    E_J = (E_J1+E_J2)*np.sqrt(math.cos(phi_e)**2 +d**2* (math.sin(phi_e)**2)) # a new Josephson energy

    phi_matrix.data = np.cos(phi_matrix.data)
    JJ = phi_matrix.multiply(-E_J)

    Hamiltonian = Capacitor + JJ

    eig_vals, eig_vec = sp.linalg.eigh(Hamiltonian.toarray())

    w_q = eig_vals[1]-eig_vals[0]
    
    return eig_vals, eig_vec, E_J, phi_array, n.toarray(), d, JJ, n_chargeoffset, w_q



eig_vals, eig_vec, E_J, phi_array, n, d, JJ, n_chargeoffset, w_q = transmon_flux(E_J1,E_J2,E_C,phi_e,N, phi_cutoff,charge_offset)

print(n)



