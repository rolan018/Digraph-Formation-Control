import numpy as np
from numpy import linalg as la


def get_f(x, params):
    mu = params.mu
    delta = params.delta
    norm_x = la.norm(x)
    f_mu = -mu * x / norm_x**3
    z = x[0, 2]
    a_j2 = 3 * delta / 2 * x / norm_x**5 * (5 * z**2 / norm_x**2 - 1) - (
        3 * delta / norm_x**5
    ) * np.array([[0, 0, z]])
    return f_mu
