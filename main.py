import logging
import numpy as np

from params import Params, ReferenceOrbit
from sat import Sat, SatType
from right_function import get_f
from integ import pk_4
from control import get_control, validate_control
from plotters import plot_c1, plot_position, plot_upr
from graph.discrete import DiscreteGraph
import matplotlib.pyplot as plt
from sat.sat_write import SatWriter
from sat.sat_reader import SatReader
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
# Init sats

sats = SatReader(reference_orbit, params).read_data("data/scenarious/5sats/data_2025-04-08T23-07-10.csv")
# .generate_data(5, True, False)
# .read_data("data/experiments/data_2025-02-09T01-13-14.csv")

########################################
# INIT PRINTERS
########################################
print(sats)

########################################
#  INTEGRATION
########################################
T_SIZE = len(t)
rng = np.random.default_rng()
# crashed_time_1 = rng.integers(low=0, high=T_SIZE//10)
# recovered_time_1 = T_SIZE//3
# # crashed_time_2 = crashed_time_1
# # recovered_time_2 = recovered_time_1
# crashed_time_2 = rng.integers(low=T_SIZE//2, high=7*T_SIZE//10)
# recovered_time_2 = rng.integers(low=crashed_time_2, high=3*T_SIZE//4)
crashed_time_1 = 1000
recovered_time_1 = 4000
crashed_time_2 = 10000000
recovered_time_2 = 10000000
print("Simulation Time:", T_SIZE)
print(f"First crashed:{crashed_time_1} {recovered_time_1}")
print(f"Second crashed:{crashed_time_2} {recovered_time_2}")
i_error_1 = 1
i_error_2 = 3
for tau in t:
    reference_orbit.integ_step(pk_4, get_f, zero_control, dt)
    dis_graph = DiscreteGraph(sat_matrix=sats, with_waights=True)
    for sat in sats:
        sat.calculate_c1()
    if tau > crashed_time_1 and tau < recovered_time_1:
        dis_graph = DiscreteGraph(sat_matrix=[sat for i, sat in enumerate(sats) if i != i_error_1 ], with_waights=True)
    if tau > crashed_time_2 and tau < recovered_time_2:
        dis_graph = DiscreteGraph(sat_matrix=[sat for i, sat in enumerate(sats) if i != i_error_2 ], with_waights=True)
    i_control = 0
    for i, sat in enumerate(sats):
        is_deactivated = False
        if tau > crashed_time_1 and tau < recovered_time_1 and i == i_error_1:
            is_deactivated = True
        elif tau > crashed_time_2 and tau < recovered_time_2 and i == i_error_2:
            is_deactivated = True
        else:
            control = get_control(dis_graph.calculate_c_diff(i_control), reference_orbit, params)
            i_control += 1
        # Delete Control from
        validated_control = validate_control(control, is_deactivated)
        sat.set_norm_control(validated_control)
        sat.integ_step(pk_4, get_f, validated_control, dt)

ft = "%Y-%m-%dT%H-%M-%S"
# SatWriter(sats).write_init_cond(f"data/experiments/data_{datetime.datetime.now().strftime(ft)}.csv")
plot_c1(sats, t, "C1", 8000, "sat_1", crashed_time_1, recovered_time_1, None, crashed_time_2, recovered_time_2)
plot_position(sats, reference_orbit, 10000)
plot_upr(sats, t, 10000)