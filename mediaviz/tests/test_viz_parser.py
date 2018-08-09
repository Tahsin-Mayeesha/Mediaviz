import pytest
import networkx as nx
from mediaviz.viz_parser import *

path = "./tests/dummy.gexf"


def generate_fake_data(path):
    G = nx.Graph()
    G.add_node(0, viz={"color":{'r':255,'g':255,'b':255},
                   "size":46,
                   "position":{"x":2,"y":3}})
    G.add_node(1, viz={"color":{'r':0,'g':0,'b':0},
                   "size":56,
                   "position":{"x":1,"y":9}})
    nx.write_gexf(G,path)
    return G




G = generate_fake_data(path=path)




def test_parse_colors():
    result = parse_colors(path)
    # check if for all nodes color codes are returned
    assert len(result.keys()) == len(G.nodes())
    # check if the results are dictionaries containing color code
    assert type(list(result.values())[0]) is dict
    result = parse_colors(path,hex=True)
    # check the returned color code is a string with hex code when hex = True
    assert type(list(result.values())[0]) is str


    




def test_parse_size():
    result = parse_size(path)
    # check if for all nodes sizes are returned
    assert len(result.keys()) == len(G.nodes())
    # check if it's returning floats

    assert type(list(result.values())[0]) is float




def test_parse_position():
    result = parse_position(path)
    # check if for all nodes positions are returned
    assert len(result.keys()) == len(G.nodes())
    # check if the results are tuples containing points for positions
    assert type(list(result.values())[0]) is tuple

