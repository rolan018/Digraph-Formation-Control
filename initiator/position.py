import numpy as np
import random

MIN=0.2
MAX=4.0
SIZE=(3,1)

def init_position_for_line(num_sats):
    # position size: (3,1)
    # point for first sat position
    init_point = np.array([[0, 1, 1]]).reshape(3, 1)
    # direction vector
    line = _random_norm_vector(MIN, MAX, SIZE)
    t=0
    for _ in range(num_sats):
        t += random.uniform(MIN, MAX)
        yield init_point + line*t

def init_position(num_sats):
    for _ in range(num_sats):
        yield np.random.uniform(low=MIN, high=MAX, size=SIZE)

def _random_norm_vector(min, max, size):
    vector = np.random.uniform(low=min, high=max, size=size)
    return vector/np.linalg.norm(vector)