import numpy as np

def cosd(degrees):
    """Compute the cosine of angles in degrees."""
    return np.cos(np.radians(degrees))

def sind(degrees):
    """Compute the sine of angles in degrees."""
    return np.sin(np.radians(degrees))

def init_vector(t, params):
    """
    Compute the reference position and velocity vectors based on time and parameters.

    Parameters:
    - t: float, time parameter
    - params: object with attributes 'rho', 'u0_p', 'Omega0_p', 'i0_p', 'omega'

    Returns:
    - xyz_vuw_p: np.ndarray, combined position and velocity vectors (6 elements)
    """
    # Extract parameters
    rho = params.rho
    u0_p = params.u0_p
    Omega0_p = params.omega0_p
    omega = params.omega
    i0_p = params.i0_p
    
    # Compute r1 vector
    angle_r1 = u0_p + (180 / np.pi) * omega * t
    r1 = rho * np.array([
        cosd(angle_r1),
        sind(angle_r1),
        0
    ])
    
    # Compute v1 vector
    v1 = rho * omega * np.array([
        -sind(angle_r1),
        cosd(angle_r1),
        0
    ])
    
    # Rotation matrix A1
    A1 = np.array([
        [cosd(-Omega0_p), sind(-Omega0_p), 0],
        [-sind(-Omega0_p), cosd(-Omega0_p), 0],
        [0, 0, 1]
    ])
    
    # Rotation matrix A2
    A2 = np.array([
        [1, 0, 0],
        [0, cosd(-i0_p), sind(-i0_p)],
        [0, -sind(-i0_p), cosd(-i0_p)]
    ])
    
    # Rotation matrix A3
    angle_A3 = -u0_p - (180 / np.pi) * omega * t
    A3 = np.array([
        [cosd(angle_A3), sind(angle_A3), 0],
        [-sind(angle_A3), cosd(angle_A3), 0],
        [0, 0, 1]
    ])
    
    # Combined rotation matrix
    A = A1 @ A2 @ A3
    
    # Compute transformed position and velocity
    xyz_p = A @ r1
    vuw_p = A @ v1
    return xyz_p.reshape(3, 1), vuw_p.reshape(3, 1)