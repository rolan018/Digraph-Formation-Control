import numpy as np
from .checkers import check_many_size

def cosd(degrees):
    """Compute the cosine of angles in degrees."""
    return np.cos(np.deg2rad(degrees))

def sind(degrees):
    """Compute the sine of angles in degrees."""
    return np.sin(np.deg2rad(degrees))

def iso_to_osk_v1(x, v, xyz_p, vuw_p, gravit_params, ref_params, tau):
    """
    Convert ISO coordinates to OSK coordinates.

    Parameters:
    - x: np.ndarray, position vector
    - v: np.ndarray, velocity vector
    - xyz_p: np.ndarray, reference position
    - vuw_p: np.ndarray, reference velocity
    - gravit_params: object with attribute 'omega'
    - ref_params: object with attributes 'Omega0_p', 'i0_p', 'u0_p'
    - tau: float, time parameter

    Returns:
    - X: np.ndarray, transformed position vector
    - V: np.ndarray, transformed velocity vector
    """
    # Rotation matrix A1
    A1 = np.array([
        [cosd(-ref_params.Omega0_p), sind(-ref_params.Omega0_p), 0],
        [-sind(-ref_params.Omega0_p), cosd(-ref_params.Omega0_p), 0],
        [0, 0, 1]
    ])
    
    # Rotation matrix A2
    A2 = np.array([
        [1, 0, 0],
        [0, cosd(-ref_params.i0_p), sind(-ref_params.i0_p)],
        [0, -sind(-ref_params.i0_p), cosd(-ref_params.i0_p)]
    ])
    
    # Calculate the angle for A3
    angle_A3 = -(ref_params.u0_p + (180 / np.pi) * gravit_params.omega * tau)
    
    # Rotation matrix A3
    A3 = np.array([
        [cosd(angle_A3), sind(angle_A3), 0],
        [-sind(angle_A3), cosd(angle_A3), 0],
        [0, 0, 1]
    ])
    
    # Combined rotation matrix A
    A = A1 @ A2 @ A3
    
    # Transform position
    X = A.T @ (x - xyz_p)
    
    # Transform velocity
    V = A.T @ (v - vuw_p) - np.cross([0, gravit_params.omega, 0], X)
    
    return X, V

def iso_to_osk_v2(x, v, ref_orbit, params):
    """
    Transforms position and velocity vectors from one coordinate system to another.

    Parameters:
    - x: numpy array of shape (1,3), position vector in the original coordinate system.
    - v: numpy array of shape (1,3), velocity vector in the original coordinate system.
    - gravit_params: object with attribute 'omega' (scalar).
    - ref_params: object with attribute 'pos_vel', a 2D numpy array of shape (6, N).
    - tau: scalar parameter.
    - i: integer index (0-based for Python).

    Returns:
    - X1: numpy array of shape (3,1), transformed position vector.
    - V1: numpy array of shape (3,1), transformed velocity vector.
    """
    #Check shape
    check_many_size(x, v, (1,3))

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
    B = np.stack((e1.T, e2.T, e3.T), axis=1).squeeze()

    # Perform vector transformations
    x1 = B.dot(x.T - xyz_p)
    v1 = B.dot(v.T - vuw_p) - np.cross(np.array([[0, omega, 0]]), x1.T).T
    
    return x1, v1
