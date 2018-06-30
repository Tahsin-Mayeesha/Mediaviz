# this has to be first to make sure that matplotlib runs in headless mode
import matplotlib
matplotlib.use("Agg")

import sys
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from fa2 import ForceAtlas2
import networkx as nx
import matplotlib.pyplot as plt

from adjustText import adjust_text

from utils import set_node_size, set_node_color, set_node_label, edgecolor_by_source,filter_graph, get_subgraph_pos
from utils import draw_networkx_nodes_custom

#from scaling import extract_correct_scale

def scale_layout(pos,scale):
    
    """ Scales layout """
    
    return { k:(v[0]*scale,v[1]*scale) for k,v in pos.items()}

def draw_force_atlas2_network(G,filename="untitled.png"):
    # extract the largest weakly connected component and convert to undirected for fa2l
    
    G = max(nx.weakly_connected_component_subgraphs(G), key=len).to_undirected()
    
    # set parameters
    
    colormap = {"right":'#e62e00',
                'center':'#ace600', 
                'center_left':'#00bfff', 
                'center_right':'#ffebe6', 
                'left':'#5d5dd5', 
                'null':'lightgray'}
    color_field = "partisan_retweet"
    size_field = 'inlink_count'
    filter_field = "inlink_count"
    label_field = "label"
    num_labels = 20 # number of labels to visualize
    k = 100 # number of nodes to visualize

    # If the size of Graph > 1000 nodes, set G to the subgraph containing largest 1000 nodes to get the layout
    
    G = filter_graph(G,filter_by=filter_field,top=1000).to_undirected()

    # extract the positions
    print("laying out with fa2l...")
    
    # calculate node sizes for whole graph to be used in layout
    sizes = set_node_size(G,size_field= "inlink_count",min_size = 0.1, max_size=200)
    # setting up scale automatic. if search failed then the position is calculated with a default scale.
    # note : set up scale and positions should be calculated in the scale script instead of the visualization script. modify later.
    #result = extract_correct_scale(G,sizes,10,100)
    #if result[0] == False:
    #    pos = force_atlas2_layout(G,
    #                             iterations=50,
    #                             pos_list=None,
    #                             node_masses=None,
    #                             outbound_attraction_distribution=False,
    #                             lin_log_mode=False,
    #                             prevent_overlapping=False,
    #                             edge_weight_influence=1.0,
    #                             jitter_tolerance=1.0,
    #                            barnes_hut_optimize=True,
    #                             barnes_hut_theta=1.0,
    #                             scaling_ratio=38,
    #                            strong_gravity_mode=False,
    #                            multithread=False,
    #                            gravity=1.0)
    #else:
    #    pos = result[2]
    #    print("scale is" + str(result[2]))
    
    print("extracted the positions")
    


    forceatlas2 = ForceAtlas2(
                          # Behavior alternatives
    
                          outboundAttractionDistribution=False,  # Dissuade hubs
                          linLogMode=False,  # NOT IMPLEMENTED
                          adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
                          edgeWeightInfluence=1.0,

                          # Performance
                          jitterTolerance=1.0,  # Tolerance
                          barnesHutOptimize=True,
                          barnesHutTheta=1.0,
                          multiThreaded=False,  # NOT IMPLEMENTED

                          # Tuning
                          scalingRatio=35.0,
                          strongGravityMode=False,
                          gravity=1.0,

                          # Log
                          verbose=True)

    positions = forceatlas2.forceatlas2_networkx_layout(G, pos=None, iterations=500)
    
    #print("Extracted the positions")
    #print(pos)
    
    pos = scale_layout(positions,2.0)

    # Extract top k nodes for visualization
    top_k_subgraph = filter_graph(G,filter_by=filter_field,top=k).to_undirected()

    # Set visual attributes
    node_colors = set_node_color(top_k_subgraph,color_by=color_field,colormap=colormap)
    node_sizes = set_node_size(top_k_subgraph,size_field= "inlink_count",min_size = 0.1, max_size=200)
    node_labels = set_node_label(top_k_subgraph,label_field = label_field)
    subgraph_pos = get_subgraph_pos(top_k_subgraph,pos)
    edge_colors = edgecolor_by_source(top_k_subgraph,node_colors)
    
    print("Drawing the visualization")
    
    # Get specific labels
    
    subset_label_nodes = sorted(zip(top_k_subgraph.nodes(),node_sizes), key= lambda x:x[1], reverse = True)[0:num_labels]
    subset_labels = {n[0]:node_labels[n[0]] for n in subset_label_nodes}
    
    # plot the visualization
    
    fig = plt.figure(figsize=(10,10),dpi=100)
    ax = fig.add_subplot(111)
    #ax.set(xlim=[0.0, 1.0], ylim=[0.0, 1.0], title='Network Viz')


    # Draw the nodes, edges, labels separately 
    
    #nodes = nx.draw_networkx_nodes(top_k_subgraph,pos=subgraph_pos,node_size=node_sizes,node_color=node_colors,                               #             alpha=.7);   
    draw_networkx_nodes_custom(top_k_subgraph,pos=subgraph_pos,node_size=node_sizes,
                               node_color=node_colors,ax=ax,alpha=0.5)
    plt.axis("scaled")
    edges = nx.draw_networkx_edges(top_k_subgraph,pos=subgraph_pos,edge_color=edge_colors,alpha=0.01);
    labels = nx.draw_networkx_labels(top_k_subgraph,pos=subgraph_pos,labels=subset_labels, font_size=8);

    # Adjust label overlapping
    
    
    x_pos = [v[0] for k,v in subgraph_pos.items()]
    y_pos = [v[1] for k,v in subgraph_pos.items()]
    adjust_text(texts = list(labels.values()), x = x_pos, y = y_pos,arrowprops=dict(arrowstyle='->', color='lightgray'))

    # Declutter visualization

    #ax.axis("off");
    
    # save the plot
    
    plt.savefig(filename)
    
    # Show the plot
    plt.show()

    
