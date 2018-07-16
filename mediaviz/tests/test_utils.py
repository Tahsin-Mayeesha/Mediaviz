import pytest
import os
import networkx as nx
from mediaviz.utils import set_node_color,set_node_size


fname = os.path.join(os.path.dirname(__file__), 'deep_state_500.gexf')
G = nx.read_gexf(fname)


def test_set_node_color():
    colormap = {"right":'#e62e00',
                'center':'#ace600', 
                'center_left':'#00bfff', 
                'center_right':'#ffebe6', 
                'left':'#5d5dd5', 
                'null':'lightgray'}
    color_field = "partisan_retweet"
    node_colors = set_node_color(G,color_by=color_field,colormap=colormap)
    # check for empty list
    assert len(node_colors)>=1
    # check if the output list length is equal to number of nodes in graph
    assert len(node_colors) == len(G.nodes())
    # assert there's no null value in the node colors
    assert None not in node_colors


def test_set_node_size():
    size_field = "inlink_count"
    min_size = 10
    max_size = 100
    node_sizes = set_node_size(G,size_field= size_field,min_size = min_size, max_size=max_size)
    # check for empty list
    assert len(node_sizes)>=1
    # check if the output list length is equal to the number of nodes in graph
    assert len(node_sizes) == len(G.nodes())
    # check if minimum and maxium values of the output is within the range given
    assert max(node_sizes) <= max_size and min(node_sizes) >= min_size
    # check if error is raised when the size_field is not in node attributes


def test_filter_graph():
    # check if it returns a graph
    # check if the number of graph nodes is equal to k
    # check if error is raised when the graph is empty
    # check if error is raised when K > number of nodes in the original graph
    pass

def test_set_node_label():
    
    # check if the number of nodes in the input graph is equal to the dictionary length
    # check if error is raised when attribute is missing for the node label
    pass

def test_edgecolor_by_source():
    # check for empty list
    # check if the number of items in the output color list is equal to number of edges in the graph
    pass


        
def test_get_subgraph_pos():
    # check if the output has positions for all nodes in the subgraph
   pass

def test_rotate():
    pass
    # check with given point if the rotation is successful
def test_rotation_layout():
    pass
    # check for empty list
    # check if the number of nodes in the rotated pos dict output is equal to number of input nodes

def test_draw_networkx_nodes_custom():
    pass