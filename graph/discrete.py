import numpy as np
from sat import Sat, SatType
from numpy import linalg
from utils import adder_edge_with_weight


def create_nodes(sat_matrix: list[Sat]):
    return [i for i in range(len(sat_matrix))]

def create_edges(sat_matrix: list[Sat]):
    edges = create_edges_with_weights(sat_matrix)
    return [(edge[0], edge[1]) for edge in edges]

def create_edges_with_weights(sat_matrix: list[Sat]):
    edges = []
    sat_distances = dict()
    for i in range(len(sat_matrix)):
        for j in range(len(sat_matrix)):
           _calculate_helper_objects(sat_matrix, edges, sat_distances, i, j)
    for second_sat in sat_distances:
        main_sat, dist = _get_min_distance(sat_distances[second_sat])
        adder_edge_with_weight(edges, main_sat, second_sat, dist)
    return edges

# Вспомогательные функции
def _calculate_helper_objects(sat_matrix: list[Sat], edges: list, sat_distances: dict, i: int, j: int):
    sat_i = sat_matrix[i]
    sat_j = sat_matrix[j]
    if i != j:
        if sat_i.sat_type == SatType.MAIN:
            if sat_j.sat_type == SatType.MAIN:
                x_i = sat_i.get_position(-1, "osk")
                x_j = sat_j.get_position(-1, "osk")
                dist = np.round(linalg.norm(x_i - x_j), 2)
                adder_edge_with_weight(edges, i, j, dist)
            else:
                x_i = sat_i.get_position(-1, "osk")
                x_j = sat_j.get_position(-1, "osk")
                if j in sat_distances:
                    sat_distances[j].append((i, np.round(linalg.norm(x_i - x_j), 2)))
                else:
                    sat_distances[j] = [(i, np.round(linalg.norm(x_i - x_j), 2))]

def _get_min_distance(distances: list):
    for i in range(len(distances)):
        if i == 0:
            i_min = i
            min_distance = distances[i][1]
        else:
            if distances[i][1] < min_distance:
                i_min = i
    return distances[i_min]
