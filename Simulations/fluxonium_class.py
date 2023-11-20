import numpy as np 
from numpy import linalg as LA
import scipy as sp 
from scipy import sparse
from scipy.sparse import linalg
from scipy.linalg import eigh

import sys
import math as math
import matplotlib 

from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib.widgets import Slider, Button
matplotlib.use('TkAgg')
# np.set_printoptions(threshold=sys.maxsize)
phi_cutoff = 3

N = 100+1

print(np.diag(np.linspace(-phi_cutoff, phi_cutoff, N)))


class Fluxonium:
    def __init__(self, E_J, E_L, E_C, N, phi_cutoff):
        self.E_J = E_J
        self.E_L = E_L
        self.E_C = E_C
        self.N = N
        self.phi_ext = np.linspace(0, 2 * np.pi, N)
        self.Phi = None
        self.Hamiltonian = None
        self.eig_vals = None
        self.eig_vecs = None
        self.a_array = None
        self.b_array = None

    def fluxonium_potential_transformation(self, E_J, E_L, phi, phi_ext):
        return -E_J * np.cos(phi - phi_ext) + 1/2 * E_L * (phi ** 2)

    def calculate_hamiltonian(self):
        delta = self.phi[3] - self.phi[2]

        # Make the matrix Phi
        self.Phi = np.diag(np.linspace(-self.phi_cutoff, self.phi_cutoff, N))

        # q^2 approximated:
        self.a_array = np.ones(self.N - 1)
        self.b_array = np.ones(self.N)
        q_2 = np.dot((np.diag(-2 * self.b_array, 0) + np.diag(self.a_array, -1) + np.diag(self.a_array, 1)), (-(1)) / (delta ** 2))

        # Conductor term: kinetic energy
        C = np.dot(4 * self.E_C, q_2)

        # JJ term: should be a positive diagonal matrix
        JJ = np.diag(self.E_J * np.cos(np.diag(self.Phi) - self.phi_ext))

        # Inductor term: positive diagonal matrix
        inductor = np.diag(0.5 * self.E_L * np.square(np.diag(self.Phi)))

        # Define the Hamiltonian
        self.Hamiltonian = C - JJ + inductor

    def solve_eigenproblem(self):
        self.eig_vals, self.eig_vecs = eigh(self.Hamiltonian)

    def get_eigenvalues(self):
        return self.eig_vals

    def get_eigenvectors(self):
        return self.eig_vecs

    def get_phi_matrix(self):
        return self.Phi

    def get_a_array(self):
        return self.a_array

    def get_b_array(self):
        return self.b_array


class Transmon:
    def __init__(self, E_J1, E_J2, E_C, phi_e, N, phi_max):
        self.E_J1 = E_J1
        self.E_J2 = E_J2
        self.E_C = E_C
        self.phi_e = phi_e
        self.N = N
        self.phi_max = phi_max
        self.Phi = None
        self.Hamiltonian = None
        self.E_J = None

    def calculate_hamiltonian(self):
        gamma = self.E_J2 / self.E_J1
        d = (gamma - 1) / (gamma + 1)
        self.E_J = (self.E_J1 + self.E_J2) * np.sqrt(math.cos(self.phi_e) ** 2 + d ** 2 * (math.sin(self.phi_e) ** 2))

        # Make the matrix Phi
        delta = 2 * abs(self.phi_max) / (self.N - 1)
        self.Phi = np.diag([-abs(self.phi_max) + delta * i for i in range(self.N)])

        # Make the matrix q
        a = np.ones(self.N - 1)
        q = np.dot((np.diag(-a, -1) + np.diag(a, 1)), (-(1j)) / (2 * delta))

        # q^2 approximated:
        a = np.ones(self.N - 1)
        b = np.ones(self.N)
        q_2 = np.dot((np.diag(-2 * b, 0) + np.diag(a, -1) + np.diag(a, 1)), (-(1)) / (delta ** 2))

        # Josephson junction
        JJ = np.diag(self.E_J * np.cos(np.diag(self.Phi)))
        self.Hamiltonian = np.dot(4 * self.E_C * np.square(1 / (2 * 1)), q_2) - JJ

    def get_hamiltonian(self):
        return self.Hamiltonian

    def get_E_J(self):
        return self.E_J

