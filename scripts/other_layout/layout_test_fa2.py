import os
import matplotlib
matplotlib.use("Agg")

import sys
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from fa2l import force_atlas2_layout
import networkx as nx
import matplotlib.pyplot as plt

from adjustText import adjust_text

from utils import set_node_size, set_node_color, set_node_label, edgecolor_by_source,filter_graph, get_subgraph_pos
from scaling import extract_correct_scale
from visualize_func import draw_force_atlas2_network



file_names  = ["climate2017","community_policing","deep_state","ebola","gun_violence",
               "network_neutrality","teenage_pregnancy","us_election","vaccines"]

for file in file_names:
    G = nx.read_gexf("data/"+file+".gexf")
    print("CURRENT NETWORK " + file)
    draw_force_atlas2_network(G,file+"_iter500.png")

