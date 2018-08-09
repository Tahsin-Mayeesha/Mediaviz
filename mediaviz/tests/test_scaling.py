import pytest
from mediaviz.scaling import *


def generate_fake_data():
    G = nx.barbell_graph(2,1) 
    pos = nx.spring_layout(G) # calculate layout with fruchterman reingold for convinience 
    node_sizes = G.degree() # set the node sizes equal to the degree of the nodes
    return G, pos, node_sizes

G, pos, node_sizes = generate_fake_data()

def test_get_distance():
    # check with random test points
    assert get_distance((0,0),(0,1)) == 1
    assert get_distance((0,0),(0,0)) == 0
    

def test_get_pairwise_distance_between_largest_nodes():
    result = get_pairwise_distance_between_largest_nodes(G, pos, node_sizes)
    # test for null values
    assert None not in result.values()

def test_get_auto_scale():
   
   # check if it returns a float value
    result = get_auto_scale(G,pos,node_sizes)
    assert type(result) is float

def test_scale_layout():
    scale = 3
    result = scale_layout(pos,scale=scale)
   # check if returned output pos dict is equal length to input
    assert len(result) == len(G.nodes())
   # check for null values
    assert None not in result.values()