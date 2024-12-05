import numpy as np
from utils import osk_to_iso
from utils import iso_to_osk_v2
from utils import check_size, check_many_size
from utils.energy import calculate_energy
from params import Params, ReferenceOrbit
from .sat_type import SatType
from c_vector import get_c1
import logging

logger = logging.getLogger(__name__)


class Sat:
    def __init__(
        self,
        xyz,
        uvw,
        sat_type: SatType,
        ref_orbit: ReferenceOrbit,
        params: Params,
        func_c1=get_c1,
    ):
        # Check correct shape
        check_many_size(xyz, uvw, (3, 1))
        # Init property
        self.position_osk = xyz
        self.velocity_osk = uvw
        self.sat_type = sat_type
        self.ref_orbit = ref_orbit
        self.params = params
        self.position_iso, self.velocity_iso = self.convert_osk_to_iso(xyz, uvw)
        # Params for control sat
        self.c1 = list()
        # function calculate c1
        self.func_c1 = func_c1
        # energy for sat
        self.energy = [calculate_energy(self.position_iso, self.velocity_iso, params)]
        # norm control 
        self.norm_control = []
    
    def integ_step(self, integrator, right_func, control, dt):
        """
        Parameters:
        - integrator: pk_4
        - dt: delta time
        """
        vector_iso = self.get_vector(-1, type="iso")
        vector_step = integrator(vector_iso, right_func, control, self.params, dt)
        position_iso = vector_step[0, :3].reshape(3, 1)
        velocity_iso = vector_step[0, 3:].reshape(3, 1)
        # Save position and velocity
        self.set_position(position_iso, type="iso")
        self.set_velocity(velocity_iso, type="iso")
        # Convert iso to osk
        position_osk, velocity_osk = self.convert_iso_to_osk(position_iso, velocity_iso)
        # Save position and velocity
        self.set_position(position_osk, type="osk")
        self.set_velocity(velocity_osk, type="osk")
        logger.info("Integrate step")
        self.energy.append(calculate_energy(position_iso, velocity_iso, self.params))
        logger.info("Calculate energy")

    def get_position(self, index: int, type: str):
        match type:
            case "osk":
                return self.position_osk[:, index].reshape((3, 1))
            case "iso":
                return self.position_iso[:, index].reshape((3, 1))
            case _:
                raise ValueError('Type must be: "osk" or "iso"')

    def set_position(self, item, type: str):
        check_size(item, (3, 1))
        match type:
            case "osk":
                self.position_osk = np.column_stack((self.position_osk, item))
            case "iso":
                self.position_iso = np.column_stack((self.position_iso, item))
            case _:
                raise ValueError('Type must be: "osk" or "iso"')

    def get_velocity(self, index: int, type: str):
        match type:
            case "osk":
                return self.velocity_osk[:, index].reshape((3, 1))
            case "iso":
                return self.velocity_iso[:, index].reshape((3, 1))
            case _:
                raise ValueError('Type must be: "osk" or "iso"')

    def set_velocity(self, item, type: str):
        check_size(item, (3, 1))
        match type:
            case "osk":
                self.velocity_osk = np.column_stack((self.velocity_osk, item))
            case "iso":
                self.velocity_iso = np.column_stack((self.velocity_iso, item))
            case _:
                raise ValueError('Type must be: "osk" or "iso"')

    def get_vector(self, index: int, type: str):
        match type:
            case "osk" | "iso":
                return np.append(
                    self.get_position(index, type),
                    self.get_velocity(index, type),
                    axis=0,
                )
            case _:
                raise ValueError('Type must be: "osk" or "iso"')

    def calculate_c1(self):
        c1 = self.func_c1(
            self.get_position(-1, "osk"), self.get_velocity(-1, "osk"), self.params
        )
        if len(self.c1) == 0:
            logger.info(f"Init c1 for sat:{c1}")
        self.c1.append(c1)

    def get_c1(self, index):
        return self.c1[index]
    
    def get_energy(self, index):
        return self.energy[index]
    
    def set_control(self, control):
        if not hasattr(self, "control"):
            logger.info(f"Init control for sat:{control}")
            self.control = control
        else:
            self.control = np.column_stack((self.control, control))
        self.norm_control.append(np.linalg.norm(control))

    def convert_iso_to_osk(self, x, v):
        check_many_size(x, v, (3, 1))
        return iso_to_osk_v2(x.T, v.T, self.ref_orbit, self.params)

    def convert_osk_to_iso(self, x, v):
        check_many_size(x, v, (3, 1))
        return osk_to_iso(x.T, v.T, self.ref_orbit, self.params)

    def __repr__(self):
        return f"Sat TYPE={self.sat_type}\nINIT POSITION=\n{self.get_position(-1, type='osk')}\nINIT VELOCITY=\n{self.get_velocity(-1, type='osk')}"
