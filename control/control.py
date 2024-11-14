import logging
import numpy as np

from params import Params, ReferenceOrbit

logger = logging.getLogger(__name__)


def get_control(c_diff: float, ref_orbit: ReferenceOrbit, params: Params):
    """
    Calculate the control vector u1 based on position, velocity, and control parameters.

    Parameters:
    - xyz_p: np.ndarray, position vector (3 elements)
    - vuw_p: np.ndarray, velocity vector (3 elements)
    - C1: float, scalar control variable
    - params: object with attributes 'C_ref' and 'k'

    Returns:
    - control_iso: np.ndarray, control vector (3 elements)
    """
    xyz_p = ref_orbit.get_last_position()
    vuw_p = ref_orbit.get_last_velocity()
    # Compute unit vectors
    e3 = xyz_p / np.linalg.norm(xyz_p)
    cross_prod = np.cross(xyz_p.T, vuw_p.T)
    e2 = (cross_prod / np.linalg.norm(cross_prod)).T
    e1 = np.cross(e2.T, e3.T).T
    # Construct transformation matrix B
    A = np.column_stack((e1, e2, e3))

    control_iso = (A @ np.array([[params.k * c_diff, 0, 0]]).reshape(3, 1)).reshape(
        1, 3
    )
    logger.info(f"C_diff:{c_diff}, control:{control_iso}")
    return control_iso
