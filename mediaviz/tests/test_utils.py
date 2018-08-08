import pytest
import os
import networkx as nx
from mediaviz.utils import *

def generate_fake_data():
    G= nx.Graph()
    G.add_node('1', partisan_retweet="right", inlink_count=15,label="Youtube")
    G.add_node('2', partisan_retweet="left", inlink_count=35,label="Facebook")
    G.add_node('3', partisan_retweet="right", inlink_count=70,label="Twitter")
    G.add_node('4', partisan_retweet="left", inlink_count=90,label="New York Times")
    G.add_edges_from([('1','2'),('1','3'),('2','4'),('3','4'),('1','4'),('2','3')])
    return G
    

G = generate_fake_data()

def test_set_node_color():

    colormap = {"right":'#e62e00',
                'left':'#5d5dd5' 
                }
    color_field = "partisan_retweet"
    node_colors = set_node_color(G,color_by=color_field,colormap=colormap)
    # check for empty list
    assert len(node_colors)>=1
    # check if the output list length is equal to number of nodes in graph
    assert len(node_colors) == len(G.nodes())
    # assert there's no null value in the node colors
    assert None not in node_colors
    # check if Keyerror is thrown when attribute for color is missing
    with pytest.raises(KeyError):
        set_node_color(G,color_by="missing attribute",colormap=colormap)


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
    with pytest.raises(KeyError):
        set_node_size(G,size_field= "missing field",min_size = min_size, max_size=max_size)


def test_filter_graph():
    k = 2
    sub_G = filter_graph(G,filter_by="inlink_count",top=k)
    # check if it returns a graph
    assert type(sub_G) == type(G)
    # check if the number of graph nodes is equal to k
    assert len(sub_G.nodes()) == k
    # check if KeyError is thrown when attribute missing in Graph node
    with pytest.raises(KeyError):
        filter_graph(G,filter_by="Missing Attribute",top=k)
    # check if error is raised when K > number of nodes in the original graph
    k = 2000
    with pytest.raises(ValueError):
        filter_graph(G,filter_by="inlink_count",top=k)

def test_set_node_label():
    label_field = "label"
    node_labels = set_node_label(G,label_field = label_field)
    # check if the number of nodes in the input graph is equal to the dictionary length
    assert len(G.nodes()) == len(node_labels)
    # check if error is raised when attribute is missing for the node label
    with pytest.raises(KeyError):
        set_node_label(G,label_field="missing_field")

def test_edgecolor_by_source():
    colormap = {"right":'#e62e00',
                'left':'#5d5dd5' 
                }
    color_field = "partisan_retweet"
    node_colors = set_node_color(G,color_by=color_field,colormap=colormap)
    edge_colors = edgecolor_by_source(G,node_colors)
    # check for empty list
    assert len(edge_colors)>=0
    # check if the number of items in the output color list is equal to number of edges in the graph
    assert len(edge_colors) == len(G.edges())


        
def test_get_subgraph_pos():
    pos  = nx.spring_layout(G)
    subgraph_nodes = G.nodes()[0:5]
    subgraph = G.subgraph(subgraph_nodes)
    subgraph_positions = get_subgraph_pos(subgraph,pos)
    # check if the output has positions for all nodes in the subgraph
    assert len(subgraph_positions) == len(subgraph_nodes)

