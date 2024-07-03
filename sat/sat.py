import numpy as np
from numpy import linalg as la


class Sat:

    def __init__(self, xyz, uvw, sat_type):
        self.xyz_osk = xyz
        self.uvw_osk = uvw
        self.sat_type = sat_type
        self.xyz_iso = np.zeros((1, 3))
        self.uvw_iso = np.zeros((1, 3))
        print(self.xyz_iso)
        print(self.xyz_osk)
        print(self.uvw_osk)

    def get_iso_to_osk(self):
        return

    def get_osk_to_iso(self, omega):
        omega_vector = np.array([[0, omega, 0]])
        cross_xyz_uvw = np.cross(self.xyz_osk[-1, :], self.uvw_osk[-1, :])
        e3 = self.xyz_osk[-1, :]/la.norm(self.xyz_osk[-1, :])
        e2 = cross_xyz_uvw/la.norm(cross_xyz_uvw)
        e1 = np.cross(e2, e3)/la.norm(np.cross(e2, e3))
        matrix_e = np.column_stack((e1, e2, e3))

        __x = np.dot(matrix_e, (self.uvw_osk + np.cross(omega_vector, self.xyz_osk[-1, :]) + self.uvw_osk).T).T
        self.xyz_iso = np.concatenate((self.xyz_iso, __x))

    def __repr__(self):
        return f"[INFO]: Sat XYZ_OSK={self.xyz_osk} UVW_OSK={self.uvw_osk } TYPE={self.sat_type}"
