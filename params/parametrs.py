"""
Parametrs for satellites
"""
from config import init_condition
import math


class Params:
    def __init__(self):
        self.k = init_condition["K"]
        self.c_ref = init_condition["C_REF"]

        self.i0_p = init_condition["I0_P"]
        self.omega0_p = init_condition["OMEGA0_P"]
        self.u0_p = init_condition["U0_P"]
        self.rho = init_condition["RHO"]

        self.mu = init_condition["MU"]
        self.m = init_condition["M"]
        self.earth_radius = init_condition["EARTH_RADIUS"]
        self.j2 = init_condition["J2"]

        self.omega = math.sqrt(self.mu/(self.rho ** 3))

        self.delta = self.j2 * self.mu * self.earth_radius ** 2

    def __repr__(self):
        return f"[INFO]: Params"
