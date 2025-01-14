from sat import Sat
import networkx as nx
import numpy as np
from .raft_utils import create_nodes, create_edges_with_weights
from graph.printers import print_graph_with_weights, print_graph

class RaftGraph:
    def __init__(self, sat_matrix: list[Sat], with_waights=False):
        self.sat_matrix = sat_matrix
        self.with_waights = with_waights
        self.__nodes = self.__init_nodes()
        self.__edges = self.__init_edges()
        self.__G = self.__init_graph()

    def __init_nodes(self):
        return RaftGraph.create_nodes(self.sat_matrix)

    def __init_edges(self):
        if self.with_waights:
            return RaftGraph.create_edges_with_weights(self.sat_matrix)
        return RaftGraph.create_edges(self.sat_matrix)

    def __init_graph(self):
        G = nx.Graph()
        G.add_nodes_from(self.__nodes)
        if self.with_waights:
            G.add_weighted_edges_from(self.__edges)
        else:
            G.add_edges_from(self.__edges)
        return G

    def calculate_c_diff(self, target: int):
        c1_for_control = []
        if target not in self.__nodes:
            raise ValueError("target must be in nodes")
        for neighbor in self.__G.neighbors(target):
            c1_for_control.append(self.sat_matrix[neighbor].get_c1(-1))
            # print(target, neighbor, self.__G.get_edge_data(neighbor, target)['weight'])
        c1_mean = np.mean(c1_for_control) if len(c1_for_control)>0 else self.sat_matrix[target].get_c1(-1)
        return c1_mean-self.sat_matrix[target].get_c1(-1)

    def get_nodes(self):
        return self.__nodes

    def get_edges(self):
        return self.__edges

    def get_graph(self):
        return self.__G
    
    def print_graph_with_weights(self):
        print_graph_with_weights(self.__G)
    
    def print_graph(self):
        print_graph(self.__G)

    @staticmethod
    def create_nodes(sat_matrix: list[Sat]):
        """
        nodes = [<node1>, <node2>, ...]
        """
        return create_nodes(sat_matrix=sat_matrix)

    @staticmethod
    def create_edges(sat_matrix: list[Sat]):
        """
        edges = [(<node1>, <node2>, <weight>), (...), ...]
        """
        edges = RaftGraph.create_edges_with_weights(sat_matrix)
        return [(edge[0], edge[1]) for edge in edges]

    @staticmethod
    def create_edges_with_weights(sat_matrix: list[Sat]):
        """
        edges = [(<node1>, <node2>, <weight>), (...), ...]
        """
        return create_edges_with_weights(sat_matrix=sat_matrix)

    def __repr__(self):
        return f"Discrete Graph for sats:{self.sat_matrix}"