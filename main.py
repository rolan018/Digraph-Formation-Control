import logging
import numpy as np

from params import Params, ReferenceOrbit
from sat import Sat, SatType
from right_function import get_f
from integ import pk_4
from control import get_control
from plotters import plot_c1, plot_position
from graph.discrete import DiscreteGraph
from initiator.position import init_position_for_line
from initiator.velocity import init_velocity
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename='satapp.log', 
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

# Init. All parameters
params = Params()

# Time period
dt = 1
T = 2 * np.pi / params.omega
t = np.arange(dt, 2*T, dt)

# Reference Orbit
reference_orbit = ReferenceOrbit(params, dt)
zero_control = np.array([[0, 0, 0]])


# Init sats
NUM_SATS = 5
sats: list[Sat] = []
for index, (position, velocity) in enumerate(zip(init_position_for_line(NUM_SATS), init_velocity(NUM_SATS))):
    sat_type = SatType.SECONDARY
    if index in (2, 4):
        sat_type = SatType.MAIN
    sats.append(Sat(position, velocity, sat_type, reference_orbit, params))

# integration
for tau in t:
    reference_orbit.integ_step(pk_4, get_f, zero_control, dt)
    dis_graph = DiscreteGraph(sat_matrix=sats, with_waights=True)
    for sat in sats:
        sat.calculate_c1()
    for i, sat in enumerate(sats):
        control = get_control(dis_graph.calculate_c_diff(i), reference_orbit, params)
        sat.integ_step(pk_4, get_f, control, dt)

plot_c1(sats, t, "C1")