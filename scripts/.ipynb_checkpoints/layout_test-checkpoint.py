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




file_names  = os.listdir("../graphs")

for file in file_names:
    G = nx.read_gexf(file)
    draw_force_atlas2_network(G,file)

