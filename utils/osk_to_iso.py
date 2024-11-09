import numpy as np
from .checkers import check_many_size


def osk_to_iso(X, V, ref_orbit, params):
    """
    Transforms position and velocity vectors using orbital parameters.

    Parameters:
    - X (1, 3): numpy array, position vector.
    - V (1, 3): numpy array, velocity vector.
    - gravit_params: object with attribute 'omega'.
    - ref_params: object with attribute 'pos_vel', a 2D numpy array.
    - tau: scalar parameter.
    - i: integer index.

    Returns:
    - x1 (3, 1): numpy array, transformed position vector.
    - v1 (3, 1): numpy array, transformed velocity vector.
    """
    # Check shape
    check_many_size(X, V, (1, 3))

    # Extract position and velocity from reference parameters
    xyz_p = ref_orbit.get_last_position()
    vuw_p = ref_orbit.get_last_velocity()
    omega = params.omega

    # Compute unit vectors
    e3 = xyz_p / np.linalg.norm(xyz_p)
    cross_prod = np.cross(xyz_p.T, vuw_p.T)
    e2 = (cross_prod / np.linalg.norm(cross_prod)).T
    e1 = np.cross(e2.T, e3.T).T

    # Construct transformation matrix B
    A = np.column_stack((e1, e2, e3))

    # Perform vector transformations
    omega_vector = np.array(
        [
            [0, omega, 0],
        ]
    )
    er = np.cross(omega_vector, X)
    v1 = np.dot(A, V.T + er.T) + vuw_p
    x1 = np.dot(A, X.T) + xyz_p

    return x1, v1
