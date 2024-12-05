import logging
import numpy as np

from params import Params, ReferenceOrbit
from sat import Sat, SatType
from sat.sat_reader import SatReader
from right_function import get_f
from integ import pk_4
from control import get_control, validate_control
from plotters import plot_c1, plot_position, plot_1d
from graph.discrete import DiscreteGraph
from initiator.printer import printer_init_vector
from initiator.position import init_position_for_line, init_position
from initiator.velocity import init_velocity
import matplotlib.pyplot as plt
from sat.sat_write import SatWriter
import datetime

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

######################################
# INIT POSITION AND VELOCITY
######################################
# Init sats with random position
NUM_SATS = 5
sats: list[Sat] = []
for index, (position, velocity) in enumerate(zip(init_position_for_line(NUM_SATS), init_velocity(NUM_SATS))):
    sat_type = SatType.SECONDARY
    # Add MAIN Sat
    if index in (2, 4):
        sat_type = SatType.MAIN
    sats.append(Sat(position, velocity, sat_type, reference_orbit, params))
# Init sats from file
# sats = SatReader(reference_orbit, params).read_data("data/experiments/data.csv")

########################################
# INIT PRINTERS
########################################
printer_init_vector(sats)

for sat in sats:
    print(sat)

########################################
#  INTEGRATION
########################################
for tau in t:
    reference_orbit.integ_step(pk_4, get_f, zero_control, dt)
    dis_graph = DiscreteGraph(sat_matrix=sats, with_waights=True)
    for sat in sats:
        sat.calculate_c1()
    for i, sat in enumerate(sats):
        control = get_control(dis_graph.calculate_c_diff(i), reference_orbit, params)
        # Delete Control from tau > T/4
        is_deactivate = tau>T/4
        validated_control = validate_control(control, is_deactivate)
        sat.integ_step(pk_4, get_f, validated_control, dt)

ft = "%Y-%m-%dT%H-%M-%S"
SatWriter(sats).write_init_cond(f"data/experiments/data_{datetime.datetime.now().strftime(ft)}.csv")
plot_c1(sats, t, "C1")
plot_position(sats)
# plot_position(sats)