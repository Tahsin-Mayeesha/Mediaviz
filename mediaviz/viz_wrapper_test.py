import networkx as nx
import os
from mediaviz.visualize import draw_forceatlas2_network

fname = os.path.join(os.path.dirname(__file__), 'deep_state_1000.gexf')
G = nx.read_gexf(fname)

draw_forceatlas2_network(G)