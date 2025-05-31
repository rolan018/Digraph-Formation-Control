import logging
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt

from params import Params, ReferenceOrbit
from sat import Sat, SatTypeRaft
from right_function import get_f
from integ import pk_4
from control import get_control, validate_control
from plotters import plot_c1, plot_position, plot_upr
from raft import ConsensusFormationControl

from initiator.printer import printer_init_vector
from initiator.position import init_position_for_line, init_position
from initiator.velocity import init_velocity

from sat.sat_reader import SatReader
from sat.sat_write import SatWriter


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
print("T:", 2*T)

# Reference Orbit
reference_orbit = ReferenceOrbit(params, dt)
zero_control = np.array([[0, 0, 0]])

######################################
# INIT POSITION AND VELOCITY
######################################
# Init sats from file
# sats = SatReader(reference_orbit, params).read_data("data/scenarious/more2sats/data_2025-03-15T01-45-47-raft.csv")
sats = SatReader(reference_orbit, params).generate_data(num_sats=5, pos_for_line=False, is_raft=True)

# sats = SatReader(reference_orbit, params).read_data("data/experiments/data_2025-02-09T01-13-14.csv")

########################################
# INIT PRINTERS
########################################
printer_init_vector(sats)


########################################
#  INTEGRATION
########################################
formation_controller = ConsensusFormationControl(sats=sats)
T_SIZE = len(t)
rng = np.random.default_rng()
crashed_time_1 = rng.integers(low=0, high=T_SIZE//10)
recovered_time_1 = T_SIZE//3
# crashed_time_2 = rng.integers(low=T_SIZE//2, high=7*T_SIZE//10)
# recovered_time_2 = rng.integers(low=crashed_time_2, high=3*T_SIZE//4)
print("Simulation Time:", T_SIZE)
print(f"First crashed:{crashed_time_1} {recovered_time_1}")
# print(f"Second crashed:{crashed_time_2} {recovered_time_2}")
for tau in t:
    reference_orbit.integ_step(pk_4, get_f, zero_control, dt)
    for sat in sats:
        sat.calculate_c1()
    formation_controller.process()
    raft_graph = formation_controller.get_graph(with_waights=True)
    for i, sat in enumerate(sats):
        control = get_control(raft_graph.calculate_c_diff(i), reference_orbit, params)
        # Delete Control
        is_deactivate = True if sat.sat_type == SatTypeRaft.CRASHED else False
        validated_control = validate_control(control, is_deactivate)
        sat.set_norm_control(validated_control)
        sat.integ_step(pk_4, get_f, validated_control, dt)
    if tau == crashed_time_1:
        # or tau == crashed_time_2:
        leader_index = formation_controller.get_leader_index()
        formation_controller.crash_leader()
    if tau == recovered_time_1: 
        # or tau == recovered_time_2:
        formation_controller.add_sat_from_last_crashed()

ft = "%Y-%m-%dT%H-%M-%S"
SatWriter(sats).write_init_cond(f"data/scenarious/5sats/data_{datetime.datetime.now().strftime(ft)}-raft.csv")
plot_c1(sats, t, -1, f"sat_{leader_index}", crashed_time_1, recovered_time_1)
plot_position(sats, reference_orbit, 10000)
plot_upr(sats, t, 10000)