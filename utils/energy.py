import numpy as np
from .checkers import check_many_size

def calculate_energy(x, v, params):
    #Check shape
    check_many_size(x, v, (3,1))
    mu = params.mu

    return np.linalg.norm(v)**2 - 2*mu/np.linalg.norm(x)