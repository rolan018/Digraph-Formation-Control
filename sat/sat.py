import numpy as np
from utils import osk_to_iso
from utils import iso_to_osk_v2
from c_vector import get_c1
from numpy import linalg as la
from utils import check_size, check_many_size
from params import Params, ReferenceOrbit

class Sat:

    def __init__(self, xyz, uvw, sat_type: int, ref_orbit:ReferenceOrbit, params: Params):
        # Check correct shape
        check_many_size(xyz, uvw, (3, 1))
        # Init property
        self.position_osk = xyz
        self.velocity_osk = uvw
        self.sat_type = sat_type
        self.ref_orbit = ref_orbit
        self.params = params
        self.c1 = get_c1(xyz, uvw, params)
        self.position_iso, self.velocity_iso = self.convert_osk_to_iso(xyz, uvw)
    
    def integ_step(self, integrator, right_func, control):
        """
        Parameters:
        - integrator: pk_4
        """
        vector_iso = self.get_last_vector(-1, type='iso')
        vector_step = integrator(vector_iso, 
                            right_func, 
                            control, 
                            self.params)
        position_iso = vector_step[0,:3].reshape(3,1)
        velocity_iso = vector_step[0,3:].reshape(3,1)
        # Save position and velocity
        self.set_position(position_iso, type='iso')
        self.set_velocity(velocity_iso, type='iso')
        # Convert iso to osk
        position_osk, velocity_osk = self.convert_iso_to_osk(position_iso, velocity_iso)
        # Save position and velocity
        self.set_position(position_osk, type='osk')
        self.set_velocity(velocity_osk, type='osk')

    def get_position(self, index: int, type: str):
        match type:
            case "osk":
                return self.position_osk[:, index].reshape((3, 1))
            case "iso":
                return self.position_iso[:, index].reshape((3, 1))
            case _:
                raise ValueError("Type must be: \"osk\" or \"iso\"")

    def set_position(self, item, type: str):
        check_size(item, (3, 1))
        match type:
            case "osk":
                self.position_osk = np.column_stack((self.position_osk, item))
            case "iso":
                self.position_iso = np.column_stack((self.position_iso, item))
            case _:
                raise ValueError("Type must be: \"osk\" or \"iso\"")
            
    def get_velocity(self, index: int, type: str):
        match type:
            case "osk":
                return self.velocity_osk[:, index].reshape((3, 1))
            case "iso":
                return self.velocity_iso[:, index].reshape((3, 1))
            case _:
                raise ValueError("Type must be: \"osk\" or \"iso\"")

    def set_velocity(self, item, type: str):
        check_size(item, (3, 1))
        match type:
            case "osk":
                self.velocity_osk = np.column_stack((self.velocity_osk, item))
            case "iso":
                self.velocity_iso = np.column_stack((self.velocity_iso, item))
            case _:
                raise ValueError("Type must be: \"osk\" or \"iso\"")
            
    def get_vector(self, index: int, type: str):
        match type:
            case "osk" | "iso":
                return np.append(self.get_position(index, type), self.get_velocity(index, type), axis=0)
            case _:
                raise ValueError("Type must be: \"osk\" or \"iso\"")

    def calculate_c1(self, position, velocity):
        c1 = get_c1(position, velocity, self.params)
        self.c1 = np.column_stack((self.c1, c1))
        return c1

    def convert_iso_to_osk(self, x, v):
        check_many_size(x, v, (3, 1))
        return iso_to_osk_v2(x.T, v.T, self.ref_orbit, self.params)

    def convert_osk_to_iso(self, x, v):
        check_many_size(x, v, (3, 1))
        return osk_to_iso(x.T, v.T, self.ref_orbit, self.params)

    def __repr__(self):
        return f"[INFO]: Sat TYPE={self.sat_type}\nINIT POSITION={self.get_position(-1, type='osk')}"
