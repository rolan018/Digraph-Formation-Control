import numpy as np
from params import Params
from utils import check_many_size

def get_c1(x, v, params: Params) -> float:
    """
    Calculate the C1

    Parameters:
    - x: np.ndarray
        Position vector with at least 3 elements. 
        x[0]: x-coordinate
        x[1]: y-coordinate
        x[2]: z-coordinate
    - v: np.ndarray
        Velocity vector with at least 3 elements.
        v[0]: velocity in x-direction
        v[1]: velocity in y-direction
        v[2]: velocity in z-direction
    - params: object
        An object containing gravitational parameters with attribute 'omega'.

    Returns:
    - C_1: float
        Calculated C1
    """
    # check shape
    check_many_size(x, v, (3,1))

    # Extract position components
    z = x[2,0]

    # Extract velocity components
    v_x = v[0,0]

    # Gravitational angular velocity
    omega = params.omega

    # Calculate c1
    return float(v_x / omega + 2 * z)

def get_c_vector(x, v, t_0, params: Params):
    """
    Calculate the C vector.

    Parameters:
    - x: np.ndarray
        Position vector with at least 3 elements. 
        x[0]: x-coordinate
        x[1]: y-coordinate
        x[2]: z-coordinate
    - v: np.ndarray
        Velocity vector with at least 3 elements.
        v[0]: velocity in x-direction
        v[1]: velocity in y-direction
        v[2]: velocity in z-direction
    - t_0: float
        Time parameter.
    - params: object
        An object containing gravitational parameters with attribute 'omega'.

    Returns:
    - C_vec: np.ndarray
        Calculated C vector as a NumPy array with 6 elements.
    """
    # Extract position components
    x_val = x[0,0]
    y = x[1,0]
    z = x[2,0]

    # Extract velocity components
    v_x = v[0,0]
    v_y = v[1,0]
    v_z = v[2,0]

    # Gravitational angular velocity
    omega = params.omega

    # Calculate each component of C_vec
    C1 = v_x / omega + 2 * z
    C2 = (v_z / omega) * np.cos(omega * t_0) - ((2 * v_x / omega) + 3 * z) * np.sin(omega * t_0)
    C3 = (v_z / omega) * np.sin(omega * t_0) + ((2 * v_x / omega) + 3 * z) * np.cos(omega * t_0)
    C4 = x_val - (2 * v_z / omega) + 3 * omega * (v_x / omega + 2 * z) * t_0
    C5 = y * np.sin(omega * t_0) + (v_y / omega) * np.cos(omega * t_0)
    C6 = y * np.cos(omega * t_0) - (v_y / omega) * np.sin(omega * t_0)

    # Combine all components into a single vector
    C_vec = np.array([C1, C2, C3, C4, C5, C6])
    return C_vec.reshape(6,1)