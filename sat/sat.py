import numpy as np
from utils import osk_to_iso
from utils import iso_to_osk_v2
from numpy import linalg as la
from params import Params

class Sat:

    def __init__(self, xyz, uvw, sat_type, params: Params):
        self.xyz_osk = xyz
        self.uvw_osk = uvw
        self.sat_type = sat_type
        self.params = params
        self.xyz_iso, self.uvw_iso = self.convert_osk_to_iso(xyz, uvw)

    def convert_iso_to_osk(self, x, v):
        return iso_to_osk_v2(x.T, v.T)

    def convert_osk_to_iso(self, x, v):
        return osk_to_iso(x.T, v.T)

    def __repr__(self):
        return f"[INFO]: Sat TYPE={self.sat_type}"
