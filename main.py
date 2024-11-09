import logging
import numpy as np

from params import Params, ReferenceOrbit
from sat import Sat, SatType
from right_function import get_f
from integ import pk_4
from control import get_control


logger = logging.getLogger(__name__)
logging.basicConfig(filename="satapp.log", level=logging.INFO)

# Init. All parameters
params = Params()

# Time period
t0 = 0
t1 = 2 * np.pi / params.omega
t1 = 5
dt = 1
t = np.linspace(t0, t1, (t1 - t0) // dt + 1)

# Reference Orbit
reference_orbit = ReferenceOrbit(params, t0)
zero_control = np.array([[0, 0, 0]])

# Init sat
x1 = np.array([[0, 1, 1]]).reshape(3, 1)

v1 = np.array([[0, 1, 1]]).reshape(3, 1)

sat1 = Sat(x1, v1, SatType.MAIN, reference_orbit, params)

for tau in t:
    reference_orbit.integ_step(pk_4, get_f, zero_control, dt)
    c1 = sat1.calculate_c1()
    control = get_control(c1, reference_orbit, params)
    sat1.integ_step(pk_4, get_f, control, dt)
