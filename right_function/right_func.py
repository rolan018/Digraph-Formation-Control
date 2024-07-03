import numpy as np
from numpy import linalg as la


def get_f(x, params):
    mu = params.mu
    delta = params.delta
    norm_x = la.norm(x)
    print(f"get_f norm_x:{norm_x}")
    f_mu = -mu*x/norm_x**3
    print(f"get_f f_mu:{f_mu}")
    z = x[0, 2]
    print(f"get_f z:{z}")
    a_j2 = 3*delta/2*x/norm_x**5 * (5*z**2/norm_x**2 - 1) - (3*delta/norm_x**5)*np.array([[0, 0, z]])
    print(f"get_f a_j2:{a_j2}")
    return f_mu + a_j2
