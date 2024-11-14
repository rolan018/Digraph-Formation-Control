from params.parametrs import Params
from sat import Sat, SatType
from integ import pk_4
import numpy as np
import networkx as nx
from params import Params, ReferenceOrbit
from graph.discrete import DiscreteGraph
from control.control import get_control
from utils.energy import calculate_energy

t0 = 0

par = Params()

# Reference Orbit
reference_orbit = ReferenceOrbit(par, t0)

# Init sat
x1 = np.array([
    [2, 4, 0]
]).reshape(3,1)
v1 = np.array([
    [1, 1, 0]
]).reshape(3,1)
sat1 = Sat(x1, v1, SatType.MAIN, reference_orbit, par)

x1 = np.array([
    [3, 4, 0]
]).reshape(3,1)
v1 = np.array([
    [2, 2, 0]
]).reshape(3,1)
sat2 = Sat(x1, v1, SatType.MAIN, reference_orbit, par)

x1 = np.array([
    [3, 2, 0]
]).reshape(3,1)
v1 = np.array([
    [3, 3, 0]
]).reshape(3,1)
sat3 = Sat(x1, v1, SatType.SECONDARY, reference_orbit, par)

x1 = np.array([
    [4, 2, 0]
]).reshape(3,1)
v1 = np.array([
    [4, 4, 0]
]).reshape(3,1)
sat4 = Sat(x1, v1, SatType.SECONDARY, reference_orbit, par)

x1 = np.array([
    [4, 4, 0]
]).reshape(3,1)
v1 = np.array([
    [5, 5, 0]
]).reshape(3,1)
sat5 = Sat(x1, v1, SatType.SECONDARY, reference_orbit, par)

x1 = np.array([
    [5, 2, 0]
]).reshape(3,1)
v1 = np.array([
    [6, 6, 0]
]).reshape(3,1)
sat6 = Sat(x1, v1, SatType.SECONDARY, reference_orbit, par)

sats = [sat1, sat2, sat3, sat4, sat5, sat6]

dis_graph = DiscreteGraph(sat_matrix=sats, with_waights=True)
G = dis_graph.get_graph()
zero_control = np.array([
    [0, 0, 0]
])

for sat in sats:
    c1 = sat.calculate_c1()

for i, sat in enumerate(sats):
    control = get_control(dis_graph.calculate_c_diff(i), reference_orbit, par)

vector = np.random.uniform(low=0.5, high=13.3, size=(1,3))
print(vector)