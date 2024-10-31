import networkx as nx
import matplotlib.pyplot as plt

def print_graph(nodes: list, edges: list):
    G = nx.Graph()

    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()

def print_graph_with_weights(nodes: list, edges: list):
    G = nx.Graph()

    G.add_nodes_from(nodes)
    G.add_weighted_edges_from(edges)

    pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=6)

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    plt.show()