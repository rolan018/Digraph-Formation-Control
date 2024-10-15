"""
Parametrs for satellites
"""
from config import init_condition
from utils import init_vector
from integ import pk_4
import math
import numpy as np

class Params:
    def __init__(self):
        self.init_condition = init_condition
        # Control. Params
        self.k = init_condition["K"]
        self.c_ref = init_condition["C_REF"]

        # Ref. Params
        self.i0_p = init_condition["I0_P"]
        self.omega0_p = init_condition["OMEGA0_P"]
        self.u0_p = init_condition["U0_P"]
        self.rho = init_condition["RHO"]

        # Grav. Params
        self.mu = init_condition["MU"]
        self.m = init_condition["M"]
        self.earth_radius = init_condition["EARTH_RADIUS"]
        self.j2 = init_condition["J2"]

        self.omega = math.sqrt(self.mu/(self.rho ** 3))

        self.delta = self.j2 * self.mu * self.earth_radius ** 2

    def __repr__(self):
        return f"[INFO]: Params({self.init_condition})"

class ReferenceOrbit:
    def __init__(self, params: Params, t0):
        self.params = params
        self.position, self.velocity = self._init_vector(t0, params)

    def _init_vector(self, t0, params: Params):
        return init_vector(t0, params)
    
    def integ_step(self, integrator, right_func, control):
        """
        Parameters:
        - integrator: pk_4
        """
        vector = integrator(np.append(self.position, self.velocity, axis=1), 
                            right_func, 
                            control, 
                            self.params)
        self.position = np.column_stack((self.position, vector[0,:3].reshape(3,1)))
        self.velocity = np.column_stack((self.velocity, vector[0,3:].reshape(3,1)))
    
    def __repr__(self):
        return f"[INFO]: ReferenceOrbit({self.params})"