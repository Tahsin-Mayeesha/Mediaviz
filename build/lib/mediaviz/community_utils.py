import random
import networkx as nx
import community

def generate_random_hex_color():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())


def get_community_colormap(partition):
    partitions = set(partition.values())
    result = {p:generate_random_hex_color() for p in partitions}
    return result

def get_community_graph(G):
    if type(G) == nx.DiGraph:
        G = max(nx.weakly_connected_component_subgraphs(G), key=len).to_undirected()
    partitions = community.best_partition(G)
    for node in G.nodes():
        G.node[node]["partition"] = partitions[node]
    return G, partitions
    