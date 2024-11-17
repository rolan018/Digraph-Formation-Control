import numpy as np

MIN=0.2
MAX=1.5
SIZE=(3,1) 

def init_velocity(num_sats):
    for _ in range(num_sats):
        yield np.random.uniform(low=MIN, high=MAX, size=SIZE)