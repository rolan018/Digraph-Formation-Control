from params.parametrs import Params
from sat import Sat, SatType
from integ import pk_4
import numpy as np
import networkx as nx
from params import Params, ReferenceOrbit
from graph.discrete import DiscreteGraph
from graph.printers import print_graph_with_weights, print_graph

t0 = 0

par = Params()

# Reference Orbit
reference_orbit = ReferenceOrbit(par, t0)

# Init sat
x1 = np.array([[2, 4, 0]]).reshape(3, 1)
v1 = np.array([[0, 1, 0]]).reshape(3, 1)
sat1 = Sat(x1, v1, SatType.MAIN, reference_orbit, par)

x1 = np.array([[3, 4, 0]]).reshape(3, 1)
v1 = np.array([[0, 1, 0]]).reshape(3, 1)
sat2 = Sat(x1, v1, SatType.MAIN, reference_orbit, par)

x1 = np.array([[3, 2, 0]]).reshape(3, 1)
v1 = np.array([[0, 1, 0]]).reshape(3, 1)
sat3 = Sat(x1, v1, SatType.SECONDARY, reference_orbit, par)

x1 = np.array([[4, 2, 0]]).reshape(3, 1)
v1 = np.array([[0, 1, 0]]).reshape(3, 1)
sat4 = Sat(x1, v1, SatType.SECONDARY, reference_orbit, par)

x1 = np.array([[4, 4, 0]]).reshape(3, 1)
v1 = np.array([[0, 1, 0]]).reshape(3, 1)
sat5 = Sat(x1, v1, SatType.SECONDARY, reference_orbit, par)

x1 = np.array([[5, 2, 0]]).reshape(3, 1)
v1 = np.array([[0, 1, 0]]).reshape(3, 1)
sat6 = Sat(x1, v1, SatType.SECONDARY, reference_orbit, par)

sats = [sat1, sat2, sat3, sat4, sat5, sat6]

dis_graph = DiscreteGraph(sat_matrix=sats, with_waights=True)
graph = dis_graph.get_graph()

target = 1
for neighbors in graph.neighbors(target):
    print(graph.get_edge_data(neighbors, target)["weight"])
