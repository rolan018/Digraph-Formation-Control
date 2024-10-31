from params.parametrs import Params
from sat import Sat, SatType
from integ import pk_4
import numpy as np
import networkx as nx
from params import Params, ReferenceOrbit
from graph.discrete import create_edges_with_weights, create_nodes, create_edges
from graph.printers import print_graph_with_weights, print_graph

t0 = 0

par = Params()

# Reference Orbit
reference_orbit = ReferenceOrbit(par, t0)

# Init sat
x1 = np.array([
    [1, 1, 0]
]).reshape(3,1)
v1 = np.array([
    [0, 1, 0]
]).reshape(3,1)
sat1 = Sat(x1, v1, SatType.SECONDARY, reference_orbit, par)

x1 = np.array([
    [2, 4, 0]
]).reshape(3,1)
v1 = np.array([
    [0, 1, 0]
]).reshape(3,1)
sat2 = Sat(x1, v1, SatType.SECONDARY, reference_orbit, par)

x1 = np.array([
    [3, 3, 0]
]).reshape(3,1)
v1 = np.array([
    [0, 1, 0]
]).reshape(3,1)
sat3 = Sat(x1, v1, SatType.MAIN, reference_orbit, par)

x1 = np.array([
    [4, 1, 0]
]).reshape(3,1)
v1 = np.array([
    [0, 1, 0]
]).reshape(3,1)
sat4 = Sat(x1, v1, SatType.SECONDARY, reference_orbit, par)

x1 = np.array([
    [5, 2, 0]
]).reshape(3,1)
v1 = np.array([
    [0, 1, 0]
]).reshape(3,1)
sat5 = Sat(x1, v1, SatType.MAIN, reference_orbit, par)

x1 = np.array([
    [6, 2, 0]
]).reshape(3,1)
v1 = np.array([
    [0, 1, 0]
]).reshape(3,1)
sat6 = Sat(x1, v1, SatType.SECONDARY, reference_orbit, par)

sats = [sat1, sat2, sat3, sat4, sat5, sat6]
edges = create_edges(sats)
nodes = create_nodes(sats)

print_graph(nodes, edges)