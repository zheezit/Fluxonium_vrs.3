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


font = {
    "family": "Liberation Sans",
    "weight": "normal",
    "stretch": "normal",
    "size": 12,
}
rc("font", **font)
rc("axes", linewidth=2)
rc("lines", linewidth=3)
c = ["#007fff", "#ff3616", "#138d75", "#7d3c98"]  # Blue, Red, Green, Purple
plt.rcParams['axes.grid'] = True
plt.rcParams['font.family'] = 'Monospace'

# Use sparce matrices

save_plots = False
show_plot = True
colors = plt.cm.Set3(np.linspace(0.3, 1.1, 8)) 



#When you have the good units, you can use these
# e = 1.60217663*10**(-19) # elementary charge in C = coulombs
# hbar = 1.05457182*10**(-34) # m2*kg/ s
# h = 6.62607015*10**(-34) # m2 kg / s


#dont care that much about the units
e = 1
hbar = 1 
h = 1

# ------------------------------------------------------------------------------------FLUXONIUM--------------------------------------------------------------------------- # 

class Fluxonium: 
    def _init_(self, C_3,E_J1,phi,phi_ext, gamma): # C_3 is the capacitanse of the capacitor
        self.E_C = e**2 /(2*C_3)
        self.E_L = (E_J1*gamma)/N
        self.delta = phi[3]-phi[2]
    
    def fluxonium_potential(self):
        return -E_J1*np.cos(phi-phi_ext)+ 1/2*self.E_L*((phi)**2)

    def fluxonium_hamiltonian(self):
        # # make our matrix phi
        Phi = np.zeros((N,N))
        for i in range(N):
            Phi[i][i]= phi[i]

        # # q^2 approximated: 
        a = np.ones((1, N-1))[0]
        b = np.ones((1,N))[0]
        q_2 = np.dot(( np.diag(-2*b,0) + np.diag(a, -1) + np.diag(a, 1)), (-(1))/(self.delta**2))
        # n_2 = np.square(1/(2*e))*q_2

        # Conductor term: kinetic energy
        C = np.dot(4*self.E_C,q_2)

        # JJ term: should be a positive diagonal matrix. 
        JJ = np.zeros((N,N))
        for i in range(N):
            JJ[i][i] = E_J1*np.cos(Phi[i][i]-phi_ext)

        # # Inductor term: positiv diagonal matrix
        inductor = np.zeros((N,N))
        for i in range(N):
            inductor[i][i] = 1/2*E_L*(Phi[i][i])**2

        #Define the Hamiltonian
        Hamiltonian = C - JJ + inductor

        eig_vals, eig_vec = sp.linalg.eigh(Hamiltonian)  
        # print(f"eigenvalues",eig_vals)
        return eig_vals,eig_vec

        

def fluxonium_potential(E_J,E_L,phi,phi_ext):
    return -E_J*np.cos(phi-phi_ext)+ 1/2*E_L*((phi)**2)


def fluxonium_hamiltonian(E_J,E_L,E_C,phi_ext,phi):
    delta = phi[3]-phi[2]
    N = len(phi)
    # # make our matrix phi
    phi_2 = np.zeros((N,N))
    for i in range(N): # now it is small phi. 
        phi_2[i][i]= phi[i]

    # # q^2 approximated: 
    a = np.ones((1, N-1))[0]
    b = np.ones((1,N))[0]
    q_2 = np.dot(( np.diag(-2*b,0) + np.diag(a, -1) + np.diag(a, 1)), (-(hbar))/(delta**2) )
    # q_2 = np.dot(( np.diag(-2*b,0) + np.diag(a, -1) + np.diag(a, 1)), (-(hbar))/(delta**2) * 1/((2*e)**2))

    # Conductor term: kinetic energy
    C = np.dot(4*E_C,q_2)

    # JJ term: should be a positive diagonal matrix. 
    JJ = np.zeros((N,N))
    for i in range(N):
        JJ[i][i] = E_J*np.cos(phi_2[i][i]-phi_ext)

    # # Inductor term: positiv diagonal matrix
    inductor = np.zeros((N,N))
    for i in range(N):
        inductor[i][i] = 1/2*E_L*(phi_2[i][i])**2

    #Define the Hamiltonian
    Hamiltonian = C - JJ + inductor

    eig_vals, eig_vec = sp.linalg.eigh(Hamiltonian)  
    # print(f"eigenvalues",eig_vals)
    return eig_vals,eig_vec


#Define initial parameters - which is also the ones i am going to find eigenvalues from!
init_phi_ext = np.pi
init_E_J = 4.
init_E_C = 1.
init_E_L = 1.
N = 100+1
Phi = np.linspace(-3*np.pi, 3*np.pi, N)
# phi = Phi*4*np.pi*e/h
phi = Phi



# if show_plot == True: 
#     # create figure 
#     fig, ax = plt.subplots(figsize=(12, 8))
#     line, = ax.plot(phi, fluxonium_potential(init_E_J, init_E_L,phi, init_phi_ext))

#     eig_vals, eig_vec = fluxonium_hamiltonian(init_E_J,init_E_L,init_E_C,init_phi_ext, phi)
#     lines = {}
#     for x in range(0, 5):
#         lines["line{0}".format(x)], = ax.plot(phi, (10*eig_vec.T[x]+eig_vals[x]), label=f"E_{x}")

#     ax.set_xlabel('\u03C6')
#     ax.set_ylabel('energy ') 
#     ax.set_ylim([-10, 40])
#     ax.set_xlim([-10,10])
#     ax.legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))
#     fig.suptitle('Energy levels of Fluxonium', fontsize=16)
    

#     # adjust the main plot to make room for the sliders
#     fig.subplots_adjust(left=0.1, bottom=0.3)

#     # Make horizontal sliders to control the phi_ext.
#     ax_phi_ext = fig.add_axes([0.1, 0.2, 0.7, 0.04])
#     phi_ext_slider = Slider(
#         ax=ax_phi_ext,
#         label='\u03C6_ext',
#         valmin=-2*np.pi,
#         valmax=2*np.pi,
#         valinit=init_phi_ext,
#     )

#     # Make horizontal sliders to control the Josephson energy.
#     ax_E_J = fig.add_axes([0.1, 0.15, 0.7, 0.04])
#     E_J_slider = Slider(
#         ax=ax_E_J,
#         label='E_J[GHz]',
#         valmin=-20.,
#         valmax=20,
#         valinit=init_E_J,
#     )

#     # Make horizontal sliders to control the induction energy.
#     ax_E_L = fig.add_axes([0.1, 0.1, 0.7, 0.04])
#     E_L_slider = Slider(
#         ax=ax_E_L,
#         label='E_L[GHz]',
#         valmin=-20.,
#         valmax=20,
#         valinit=init_E_L,
#     )

#     # Make horizontal sliders to control the capacitor energy.
#     ax_E_C = fig.add_axes([0.1, 0.05, 0.7, 0.04])
#     E_C_slider = Slider(
#         ax=ax_E_C,
#         label='E_C[GHz]',
#         valmin=-20.,
#         valmax=20,
#         valinit=init_E_C,
#     )


#     # The function to be called anytime a slider's value changes
#     def update(val):
#         line.set_ydata(fluxonium_potential(E_J_slider.val, E_L_slider.val,phi, phi_ext_slider.val))
#         eig_vals, eig_vec = fluxonium_hamiltonian(E_J_slider.val,E_L_slider.val, E_C_slider.val,phi_ext_slider.val, phi)
#         for x in range(0, 5):
#             lines["line{0}".format(x)].set_ydata(10*eig_vec.T[x]+eig_vals[x])
#         fig.canvas.draw_idle()


#     phi_ext_slider.on_changed(update)
#     E_J_slider.on_changed(update)
#     E_L_slider.on_changed(update)
#     E_C_slider.on_changed(update)

#     # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
#     resetax = fig.add_axes([0.8, 0.0, 0.1, 0.04])
#     button = Button(resetax, 'Reset', hovercolor='0.975')


#     def reset(event):
#         phi_ext_slider.reset()
#         E_J_slider.reset()
#         E_L_slider.reset()
#         E_C_slider.reset()
#     button.on_clicked(reset)


# plt.show()





# -----------------------------------------------------------------------------------NEW_FLUXONIUM---------------------------------------------------------------------#


#Define fluxonium potential
def new_fluxonium_potential(E_J,E_NL,phi,phi_ext):
    return -E_J*np.cos(phi-phi_ext)+(1/2)*E_NL*((phi)**4)


def new_fluxonium_hamiltonian(E_J,E_NL,E_C,phi_ext,phi):
    delta = phi[3]-phi[2]
    N = len(phi)

    # # make our matrix phi
    phi_2 = np.zeros((N,N)) # Make an emty matrix NxN large
    for i in range(N):
        phi_2[i][i]= phi[i] # fill in the values of the Phi in the diagonal. 

    # # q^2 approximated: 
    a = np.ones((1, N-1))[0]
    b = np.ones((1,N))[0]
    q_2 = np.dot(( np.diag(-2*b,0) + np.diag(a, -1) + np.diag(a, 1)), (-(1))/(delta**2))
    # n_2 = np.square(1/(2*e))*q_2

    # Capacitor term: kinetic energy
    C = np.dot(4*E_C,q_2)

    # JJ term: should be a positive diagonal matrix. 
    JJ = np.zeros((N,N))
    for i in range(N):
        JJ[i][i] = E_J*np.cos(phi_2[i][i]-phi_ext)

    # # Inductor term: positiv diagonal matrix
    quarton = np.zeros((N,N))
    for i in range(N):
        quarton[i][i] = 1/2*E_NL*(phi_2[i][i])**4

    #Define the Hamiltonian
    Hamiltonian = C - JJ + quarton

    eig_vals, eig_vec = sp.linalg.eigh(Hamiltonian)  
    # print(f"eigenvalues",eig_vals)
    return eig_vals,eig_vec




#Define initial parameters - which is also the ones i am going to find eigenvalues from!
init_phi_ext = np.pi
init_E_J = 4.
init_E_C = 1.
init_E_L = 1.
N = 100+1
Phi = np.linspace(-3*np.pi, 3*np.pi, N)
# phi = Phi*4*np.pi*e/h
phi = Phi



if show_plot == True: 
    # create figure 
    fig, ax = plt.subplots(figsize=(12, 8))
    line, = ax.plot(phi, new_fluxonium_potential(init_E_J, init_E_L,phi, init_phi_ext))

    eig_vals, eig_vec = new_fluxonium_hamiltonian(init_E_J,init_E_L,init_E_C,init_phi_ext, phi)
    lines = {}
    for x in range(0, 5):
        lines["line{0}".format(x)], = ax.plot(phi, (10*eig_vec.T[x]+eig_vals[x]), label=f"E_{x}")

    ax.set_xlabel('\u03C6')
    ax.set_ylabel('energy ') 
    ax.set_ylim([-10, 40])
    ax.set_xlim([-10,10])
    ax.legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))
    fig.suptitle('Energy levels of Fluxonium', fontsize=16)
    

    # adjust the main plot to make room for the sliders
    fig.subplots_adjust(left=0.1, bottom=0.3)

    # Make horizontal sliders to control the phi_ext.
    ax_phi_ext = fig.add_axes([0.1, 0.2, 0.7, 0.04])
    phi_ext_slider = Slider(
        ax=ax_phi_ext,
        label='\u03C6_ext',
        valmin=-2*np.pi,
        valmax=2*np.pi,
        valinit=init_phi_ext,
    )

    # Make horizontal sliders to control the Josephson energy.
    ax_E_J = fig.add_axes([0.1, 0.15, 0.7, 0.04])
    E_J_slider = Slider(
        ax=ax_E_J,
        label='E_J[GHz]',
        valmin=-20.,
        valmax=20,
        valinit=init_E_J,
    )

    # Make horizontal sliders to control the induction energy.
    ax_E_L = fig.add_axes([0.1, 0.1, 0.7, 0.04])
    E_L_slider = Slider(
        ax=ax_E_L,
        label='E_L[GHz]',
        valmin=-20.,
        valmax=20,
        valinit=init_E_L,
    )

    # Make horizontal sliders to control the capacitor energy.
    ax_E_C = fig.add_axes([0.1, 0.05, 0.7, 0.04])
    E_C_slider = Slider(
        ax=ax_E_C,
        label='E_C[GHz]',
        valmin=-20.,
        valmax=20,
        valinit=init_E_C,
    )


    # The function to be called anytime a slider's value changes
    def update(val):
        line.set_ydata(new_fluxonium_potential(E_J_slider.val, E_L_slider.val,phi, phi_ext_slider.val))
        eig_vals, eig_vec = new_fluxonium_hamiltonian(E_J_slider.val,E_L_slider.val, E_C_slider.val,phi_ext_slider.val, phi)
        for x in range(0, 5):
            lines["line{0}".format(x)].set_ydata(10*eig_vec.T[x]+eig_vals[x])
        fig.canvas.draw_idle()


    phi_ext_slider.on_changed(update)
    E_J_slider.on_changed(update)
    E_L_slider.on_changed(update)
    E_C_slider.on_changed(update)

    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    resetax = fig.add_axes([0.8, 0.0, 0.1, 0.04])
    button = Button(resetax, 'Reset', hovercolor='0.975')


    def reset(event):
        phi_ext_slider.reset()
        E_J_slider.reset()
        E_L_slider.reset()
        E_C_slider.reset()
    button.on_clicked(reset)


plt.show()

