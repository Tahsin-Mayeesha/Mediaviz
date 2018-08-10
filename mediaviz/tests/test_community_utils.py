import pytest
import random
import networkx as nx
import community
from mediaviz.community_utils import *

def generate_fake_graph():
    G = nx.barbell_graph(4,1) # create a barbell graph because they have good community structure 
    return G

    

def test_get_community_graph():
    G = generate_fake_graph()
    G, partitions = get_community_graph(G)
    # check all nodes of G has partition in it's attribute
    assert len([d['partition'] for n, d in G.nodes(data=True)]) == len(G.nodes())
    # check if the dictionary containing partitions has all the nodes
    assert len(partitions) == len(G.nodes())
    
    
def test_get_community_colormap():
    G = generate_fake_graph()
    G, partitions = get_community_graph(G)
    colormap = get_community_colormap(partitions)
    # check if the colormap has all the unique partition groups as keys
    assert len(colormap.values()) == len(set(partitions.values()))