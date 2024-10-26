from params import Params, ReferenceOrbit
from sat import Sat
from c_vector import get_c_vector
from right_function import get_f
from integ import pk_4
import numpy as np

# Init. All parameters
params = Params()

# x0 = np.array([
#     [0, 1, 1]
# ]).reshape(3,1)
# v0 = np.array([
#     [1,0,0]
# ]).reshape(3,1)
# sat = Sat(x0, v0, 1, par)

# upr = np.array([
#     [0, 0, 0]
# ])

# x1 = pk_4(np.append(x0.T, v0.T, axis=1), get_f, upr, par)

# c = get_c_vector(x0, v0,0, par)
# print(c)

# Time period
t0 = 0
t1 = 2*np.pi/params.omega
t1 = 5
dt = 1
t = np.linspace(t0, t1, (t1-t0) // dt + 1)

# Reference Orbit
reference_orbit = ReferenceOrbit(params, t0)
zero_control = np.array([
    [0, 0, 0]
])

for i in range(len(t)):
    reference_orbit.integ_step(pk_4, get_f, zero_control)
    if i==3:
        print(f"START:{reference_orbit.get_position(0)}")
        print(f"FINISH:{reference_orbit.get_last_position()}")