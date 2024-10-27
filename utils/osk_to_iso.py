import numpy as np

def osk_to_iso(X, V):
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
    #Check shape
    if X.shape != (1, 3) or V.shape != (1, 3):
            raise ValueError("\"X\" or \"V\" size must be: (1, 3)")

    # Extract position and velocity from reference parameters
    # xyz_p = ref_params.pos_vel[0:3, i]
    # vuw_p = ref_params.pos_vel[3:6, i]
    # omega = gravit_params.omega
    xyz_p = np.array([
        [1, 1, 0],
    ]).reshape(3,1)
    vuw_p = np.array([
        [1, 1, 1],
    ]).reshape(3,1)
    omega = 2

    # Compute unit vectors
    e3 = xyz_p / np.linalg.norm(xyz_p)
    cross_prod = np.cross(xyz_p.T, vuw_p.T)
    e2 = (cross_prod / np.linalg.norm(cross_prod)).T
    e1 = np.cross(e2.T, e3.T).T

    # Construct transformation matrix B
    A = np.column_stack((e1, e2, e3))

    # Perform vector transformations
    omega_vector = np.array([
        [0, omega, 0],
    ])
    er = np.cross(omega_vector, X)
    v1 = np.dot(A, V.T + er.T) + vuw_p
    x1 = np.dot(A, X.T) + xyz_p

    return x1, v1