import math
from itertools import combinations
from fa2l import force_atlas2_layout
import networkx as nx


def _get_distance(pos1, pos2):
    """ Returns distance between two points

    Params : 

    pos1 : tuple in (x,y) format
    pos2 : tuple in (x,y) format

    """
    return math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)


def _get_pairwise_distance_between_largest_nodes(G, pos, node_sizes, k=20):
    """ 
    Boolean. Returns the distances between top k largest nodes

    Parameters  
    ----------

    G : A graph object
    pos : dict containing the position of the nodes
    k : number of nodes to consider

    Returns 
    -------

    Returns the dictionary containing the distance between the top k largest nodes.  
    """
    top_k_nodes = [n[0] for n in sorted(
        node_sizes.items(), key=lambda x:x[1], reverse=True)[0:k]]
    distances = {}
    for n1, n2 in combinations(top_k_nodes, 2):
        distances[(n1, n2)] = _get_distance(pos[n1], pos[n2])

    return distances


def get_auto_scale(G, pos, node_sizes, k=20):
    """ Returns the ratio of the ideal vs current top node distance.

    The scale is being set with a heuristic that we consider k largest nodes to prevent overlap,
    take the distances of all these nodes, find the current minimum top node distance. We also 
    find the ideal minimum top node distance that will prevent overlap and return their ratio to scale
    the layout by that scale.
    
    Parameters
    ----------

    G : nx.Graph

        A networkx Graph
    
    pos : dict

        A dictionary containing the node positions
    
    node_sizes : dict

        A dictionary containing the node sizes.
    
    k : int, default 20.

        Number of nodes to consider when setting the scale automatically.
    
    """
    result = _get_pairwise_distance_between_largest_nodes(
        G, pos, node_sizes, k=20)
    current_minimum_top_node_distance = min(result.values())
    nodes = min(result, key=result.get)
    ideal_minimum_top_node_distance = node_sizes[nodes[0]
                                                 ] + node_sizes[nodes[1]] + 50
    return ideal_minimum_top_node_distance/current_minimum_top_node_distance


def scale_layout(pos, scale):
    """ Scales layout
    
    Parameters
    ----------
    
    pos: dict
        A dictionary containing the positions of the nodes.
        
    scale :  int or float.
        
        Number to scale the positions by. 
        
    Returns
    -------
    dict

        Returns Dictionary containing Positions for the nodes scaled by the scale.
    
    """

    return {k: (v[0]*scale, v[1]*scale) for k, v in pos.items()}
