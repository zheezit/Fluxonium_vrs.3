import numpy as np
import scipy.special
import math
from decimal import Decimal, getcontext

# Set the precision (number of decimal places)
getcontext().prec = 50
# This script works for dielectric resonators

#When you have the good units, you can use these
# e = 1.60217663*10**(-19) # elementary charge in C = coulombs
# hbar = 1.05457182*10**(-34) # m2*kg/ s
# h = 6.62607015*10**(-34) # m2 kg / s


#dont care that much about the units
# e = 1
# hbar = 1 
# h = 1

#Planck's constant (h) in J*s (joule seconds)
h = 6.62607015e-34  # Planck constant


# Reduced Planck's constant (h-bar or ħ) in J*s (joule seconds)
h_bar = h / (2 * 3.141592653589793)  # h / (2 * pi)



# Elementary charge (e) in coulombs
e = 1.602176634e-19
epislon_naught = 8.854187817e-12 # farads per meter


class Resonator_Material_prop:
    def __init__(self, name, relative_permittivity, s, w,t, loss_tangent, conductivity):
        self.name = name                                    # The name of the material
        self.relative_permittivity = relative_permittivity  #
        self.s = s                                          #                                       
        self.w = w                                          #
        self.a = w
        self.b = 2*self.s + self.w                          #
        self.t = t                                          #
        self.loss_tangent = loss_tangent                    # 
        self.conductivity = conductivity                    #S/m (at 20 degrees) although we dont really need it, because it is superconducting. 
        

    def calculate_effective_dielectric_constant(self):
        k = self.w/self.b
        # print(k)
        k_m = np.sqrt(1-k**2)
        # print(k_m)
        tanh_func = lambda x: np.tanh(((np.pi*x))/np.log((4*h)))
        # print(np.log(math.pi*self.a)/np.log(4*h))
        # print(np.pi*self.a/(4*h)*1e-28)
        # print(np.pi*self.b/(4*h)*1e-28)
        k_3 = tanh_func(self.a)/tanh_func(self.b)
        # print(k_3)       
        k_3 = 0.952142908754
        # print(k_3**2)
        k_3m = np.sqrt(np.abs(1-k_3**2))
        # print(k_3m)
        # print((scipy.special.ellipk(k_m)*scipy.special.ellipk(k_3)))
        K_tilde = (scipy.special.ellipk(k_m)*scipy.special.ellipk(k_3))/(scipy.special.ellipk(k)*scipy.special.ellipk(k_3m))
        print(K_tilde)
        effective_epsilon = (1 + self.relative_permittivity * K_tilde) / (1 + K_tilde)
        return effective_epsilon
    
    def geometric_factor(self):
        k = self.a/self.b
        K = scipy.special.ellipk(k)
        g = 1/(2*k**2 *K**2) *(-np.log(self.t/(4*self.w)) + 2*(self.w + self.s)/(self.w + 2*self.s) *np.log(self.s/(self.w+self.s))- self.w/(self.w +2*self.s)*np.log(self.t/(4*(self.w+2*self.s))))
        print("schuster says the geometric factor is around 5")
        return g
    
    def kinetic_inductance(self):
        L_k = 
        return 4
    
    # def calculate_capacitance(self):
    #     C = 4*

    
    # def calculate_approximate_unloaded_Q(self):
    #     Q_d = 

    def get_properties(self):
        properties = {
            "Material Name": self.name,
            "Relative Permittivity": self.relative_permittivity,
            "Effective Dielectric Constant": self.calculate_effective_dielectric_constant(),
            "Geometric factor": self.geometric_factor(),
        }
        return properties
    


# All the informations written down for aluminium is found in Pozar2012

# def __init__(self, name, relative_permittivity, s, a,t, loss_tangent, conductivity):
Aluminium = Resonator_Material_prop("Aluminium", 
                                    relative_permittivity= 9.5, # between 9.5-10 for 99.5%
                                    s = 6e-6, # meters
                                    w =  10.7e-6, #meters
                                    t = 200e-9, #meters
                                    loss_tangent=0.0003,
                                    conductivity= 3.816*10**7)
# material2 = Resonator_Material_prop("Material B", 3.2, 0.18, (2e9, 8e9))
# NbTiN = Resonator_Material_prop("NbTiN",
#                                 relative_permittivity= 9.5, # between 9.5-10 for 99.5%
#                                 s = 2e-6, # meters
#                                 w =  29.4e-6, #meters
#                                 t = 20e-9, #meters
#                                 loss_tangent=0.0003,
#                                 conductivity= 3.816*10**7)

print(Aluminium.get_properties())
