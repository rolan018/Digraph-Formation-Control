import numpy as np
from sat import Sat, SatTypeRaft
from graph.utils import adder_edge_with_weight


def create_nodes(sat_matrix: list[Sat]):
    return [i for i in range(len(sat_matrix))]


def create_edges_with_weights(sat_matrix: list[Sat]):
    edges = []
    for i in range(len(sat_matrix)):
        if sat_matrix[i].sat_type == SatTypeRaft.LEADER:
            for j in range(len(sat_matrix)):
                if i != j and sat_matrix[j].sat_type != SatTypeRaft.CRASHED:
                    x_i = sat_matrix[i].get_position(-1, "osk")
                    x_j = sat_matrix[j].get_position(-1, "osk")
                    dist = np.round(np.linalg.norm(x_i - x_j), 2)
                    adder_edge_with_weight(edges, i, j, dist)
    return edges
