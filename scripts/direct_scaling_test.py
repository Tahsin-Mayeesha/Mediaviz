# this has to be first to make sure that matplotlib runs in headless mode
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
from utils import draw_networkx_nodes_custom
#from scaling import extract_correct_scale

import math
from itertools import combinations

def get_distance(pos1,pos2):
    """ Returns distance between two points
    
    Params : 
    
    pos1 : tuple in (x,y) format
    pos2 : tuple in (x,y) format
    
    """
    return math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)

    

def get_pairwise_distance_between_largest_nodes(G,pos,node_sizes,k=20):
    """ 
    Boolean. Returns the distances between top k largest nodes
    Parameters : 
    ____________
    
    G : A graph object
    pos : dict containing the position of the nodes
    k : number of nodes to consider    
    """
    top_k_nodes = [n[0] for n in sorted(node_sizes.items(),key=lambda x:x[1], reverse = True)[0:k]]
    top_k_pos = {k:v for k,v in pos.items() if k in top_k_nodes}
    distances = {}
    for n1,n2 in combinations(top_k_nodes,2):
        distances[(n1,n2)]=get_distance(pos[n1],pos[n2])
            
    return distances


def direct_scaling_ratio(G,pos,node_sizes,ideal_distance = 450,k=20):
    """ Returns the ratio of the ideal vs current top node distance """
    result = get_pairwise_distance_between_largest_nodes(G,pos,node_sizes,k=20)
    current_minimum_top_node_distance = min(result.values())
    nodes = min(result,key=result.get)
    ideal_minimum_top_node_distance = node_sizes[nodes[0]] + node_sizes[nodes[1]] + 50
    #return ideal_minimum_top_node_distance/current_minimum_top_node_distance
    return ideal_distance/current_minimum_top_node_distance
    

def scale_layout(pos,scale):
    
    """ Scales layout """
    
    return { k:(v[0]*scale,v[1]*scale) for k,v in pos.items()}

def main():
    if len(sys.argv) < 2:
        sys.exit('usage: %s < input gexf' % sys.argv[0])

    # Input Graph file 

    infile = sys.argv[1]

    G = nx.read_gexf(infile)
    
    # extract the largest weakly connected component and convert to undirected for fa2l
    
    G = max(nx.weakly_connected_component_subgraphs(G), key=len).to_undirected()
    
    # set parameters
    
    colormap = {"right":'#e62e00',
                'center':'#ace600', 
                'center_left':'#00bfff', 
                'center_right':'#ffebe6', 
                'left':'#5d5dd5', 
                'null':'darkgray'}
    color_field = "partisan_retweet"
    size_field = 'inlink_count'
    filter_field = "inlink_count"
    label_field = "label"
    num_labels = 20 # number of labels to visualize
    k = 100 # number of nodes to visualize

    # If the size of Graph > 1000 nodes, set G to the subgraph containing largest 1000 nodes to get the layout
    
    # G = filter_graph(G,filter_by=filter_field,top=1000).to_undirected()

    # extract the positions
    print("laying out with fa2l...")
    
    # calculate node sizes for whole graph to be used in layout
    #node_sizes = set_node_size(G,size_field= "inlink_count",min_size = 0.1, max_size=800)
    # setting up scale automatic. if search failed then the position is calculated with a default scale.
    # note : set up scale and positions should be calculated in the scale script instead of the visualization script. modify later.
    #result = extract_correct_scale(G,node_sizes,10,100)
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
    #                             barnes_hut_optimize=True,
    #                             barnes_hut_theta=1.0,
    #                             scaling_ratio=38,
    #                            strong_gravity_mode=False,
    #                            multithread=False,
    #                            gravity=1.0)
    #else:
    #    pos = result[2]
    
    
    fa2l_pos = force_atlas2_layout(G,
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
                              scaling_ratio=40,
                              strong_gravity_mode=False,
                              multithread=False,
                              gravity=1.0)
    
    
    
    print("Extracted the positions")
    
    original_node_sizes = dict(zip(G.nodes(),set_node_size(G,size_field= "inlink_count",min_size = 0.1, max_size=200)))

    scale = direct_scaling_ratio(G,fa2l_pos,original_node_sizes,k=20)
    print("scale : " + str(scale))
    #print(pos)
    
    # scaling the position
    
    pos = scale_layout(fa2l_pos,scale)

    # Extract top k nodes for visualization
    top_k_subgraph = filter_graph(G,filter_by=filter_field,top=k).to_undirected()

    # Set visual attributes
    node_sizes = set_node_size(top_k_subgraph,size_field= "inlink_count",min_size = 10, max_size=200)
    node_colors = set_node_color(top_k_subgraph,color_by=color_field,colormap=colormap)
    node_labels = set_node_label(top_k_subgraph,label_field = label_field)
    subgraph_pos = get_subgraph_pos(top_k_subgraph,pos)
    edge_colors = edgecolor_by_source(top_k_subgraph,node_colors)
    
    print("Drawing the visualization")
    
    # Get specific labels
    
    subset_label_nodes = sorted(zip(top_k_subgraph.nodes(),node_sizes), key= lambda x:x[1], reverse = True)[0:num_labels]
    subset_labels = {n[0]:node_labels[n[0]] for n in subset_label_nodes}
    
    # plot the visualization
    
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    ax.set(xlim=[-10000, 10000], ylim=[-10000, 10000])


    # Draw the nodes, edges, labels separately 
    
    #nodes = nx.draw_networkx_nodes(top_k_subgraph,pos=subgraph_pos,node_size=node_sizes,node_color=node_colors,             #                               alpha=.7);
    
    draw_networkx_nodes_custom(top_k_subgraph,pos=subgraph_pos,node_size=node_sizes,
                               node_color=node_colors,ax=ax,alpha=0.9)
    plt.axis("scaled")
    edges = nx.draw_networkx_edges(top_k_subgraph,pos=subgraph_pos,edge_color=edge_colors,alpha=0.01);
    labels = nx.draw_networkx_labels(top_k_subgraph,pos=subgraph_pos,labels=subset_labels, font_size=6);
    #plt.axis('scaled')


    # Adjust label overlapping
    
    
    x_pos = [v[0] for k,v in subgraph_pos.items()]
    y_pos = [v[1] for k,v in subgraph_pos.items()]
    adjust_text(texts = list(labels.values()),arrowprops=dict(arrowstyle='->', color='lightgray'))

    # Declutter visualization

    #ax.axis("off");
    
    # save the plot
    
    plt.savefig("untitled.png")
    
    # Show the plot
    plt.show()

    
main()
