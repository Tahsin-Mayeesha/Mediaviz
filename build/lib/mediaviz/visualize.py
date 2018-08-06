import warnings
warnings.filterwarnings('ignore')

# this has to be first to make sure that matplotlib runs in headless mode
import matplotlib
matplotlib.use("Agg")
import numpy as np
from fa2l import force_atlas2_layout
import networkx as nx
import matplotlib.pyplot as plt
from adjustText import adjust_text

from .utils import set_node_size, set_node_color, set_node_label, edgecolor_by_source, filter_graph, get_subgraph_pos
from .utils import draw_networkx_nodes_custom
from .scaling import get_auto_scale, scale_layout
from .draw import draw_networkx_graph_customized


def draw_forceatlas2_network(G, filename="untitled.png"):
    # extract the largest weakly connected component and convert to undirected for fa2l

    G = max(nx.weakly_connected_component_subgraphs(G), key=len).to_undirected()

    # set parameters

    colormap = {"right": '#e62e00',
                'center': '#ace600',
                'center_left': '#00bfff',
                'center_right': '#ffebe6',
                'left': '#5d5dd5',
                'null': 'lightgray'}
    
    # extract the positions
    
    fa2l_pos = force_atlas2_layout(
        G,
        iterations=50,
        pos_list=None,
        node_masses=None,
        outbound_attraction_distribution=False,
        lin_log_mode=False,
        prevent_overlapping=False,
        edge_weight_influence=1.0,
        jitter_tolerance=1.0,
        barnes_hut_optimize=True,
        barnes_hut_theta=1.0,
        scaling_ratio=38,
        strong_gravity_mode=False,
        multithread=False,
        gravity=1.0)


    # needed to calculate the top 20 largest nodes first
    original_node_sizes = dict(zip(G.nodes(), set_node_size(
        G, size_field="inlink_count", min_size=0.1, max_size=200)))

    scale = get_auto_scale(G, fa2l_pos, original_node_sizes, k=20)
    print("scale : " + str(scale))
    # print(pos)

    # scaling the position

    pos = scale_layout(fa2l_pos, scale)
    
    
    # draw the network
    
    draw_networkx_graph_customized(
        G,
        pos=pos,
        num_nodes=100, num_labels=20,
        color_by="partisan_retweet", colormap=colormap,
        size_field="inlink_count", min_size=0.1, max_size=200,
        with_labels=True, label_field="label",
        filter_by="inlink_count", top=100,
        adjust_labels=True,
        node_opacity=0.5, edge_opacity=0.01,
        font_size=8,
        filename="untitled.png", title="Deep State",
        edge_color_by_source=True,
        figsize=(10, 10))
