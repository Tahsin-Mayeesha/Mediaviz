import random
import networkx as nx
import community

def _generate_random_hex_color():
    """ Generates handom hex color code and returns them as string
    
    Helper function for setting community colormaps. Does not take any input.
    
    Returns
    -------
    str
        hex code. Example : "#FFFFFF". 

    """
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())


def get_community_colormap(partition):
    """Takes dict of partitions after community detection and returns dict with colormap for partitions.

    The function is currently used with python-louvain package, but it's a general purpose function
    for randomly generating colorlaps from node attributes.Expected to change into 
    get_random_colormap(node_attributes) in the next version.

    Parameters
    ----------
    partition : dict
        Dictionary of form {node1:partition,node2:partition....} generated after community detection.
    
    Examples
    --------
    >>> import community #python-louvain package
    >>> import networkx as nx
    >>> from mediaviz.community_utils import get_community_colormap
    >>> G = nx.florentine_families_graph()
    >>> partitions = community.best_partition(G)
    >>> get_community_colormap(partitions)
    {0: '#A0FD29', 1: '#C3E994', 2: '#61EDD2', 3: '#DCB0DF'}



    Returns
    -------
    dict
        Dictionary containing partitions and colormaps. 

    """
    partitions = set(partition.values())
    result = {p:_generate_random_hex_color() for p in partitions}
    return result

def get_community_graph(G):
    """ Takes a Graph, generates partitions from python-louvain package, sets the partitions as node
    attributes and returns the Graph and partitions.

    Helper function to integrate community detection with the draw function. In the draw function color_by
    parameter takes a node attribute along with a colormap for the attributes. So here python-louvain is used
    for getting the community partitions first and then we set those partitions as node attributes. 

    Examples 
    --------
    >>> import networkx as nx
    >>> G = nx.florentine_families_graph()
    >>> from mediaviz.community_utils import get_community_graph
    >>> G, partitions = get_community_graph(G)

    Parameters
    ----------
    G : nx.Graph
        A networkx graph.
    
    Notes 
    -----

    If G is a digraph , as python-louvain package does not currently support digraphs, it's changed to the 
    undirected graph of the largest weakly connected component.See source if necessary.

    Returns
    -------
    tuple 
        Returns a tuple of form (G, partitions) where G has partitions set as node attributes and 
        partitions are partitions generated from the python-louvain package. 

    """
    if type(G) == nx.DiGraph:
        G = max(nx.weakly_connected_component_subgraphs(G), key=len).to_undirected()
    partitions = community.best_partition(G)
    for node in G.nodes():
        G.node[node]["partition"] = partitions[node]
    return G, partitions
    