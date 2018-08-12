
def set_node_color(G, color_by, colormap=None):
    """ Returns a list of colors for each node based on the provided colormap. 

    Parameters 
    ----------

    G : graph.
        A networkx graph.

    color_by : str
        Graph node attribute with finite discrete categorical values.
        See : https://networkx.github.io/documentation/networkx-1.10/tutorial/tutorial.html#adding-attributes-to-graphs-nodes-and-edges for learning about node attributes

    colormap : 
        Dict mapping values of color_by attribute to different colors. colors can be a single color like 'r' or
        hex code of form '#FFFFFF'

    Returns
    -------
    list
        A list containing the colors for each node.

    Example 
    -------

    >>> colormap = {'male':'b','female':'r'}
    >>> node_colors = set_node_color(G,"gender",colormap)
    ['b','b','r','b']
    """
    node_colors = [colormap[n[1][color_by]] for n in G.nodes(data=True)]
    return node_colors


def set_node_size(G, size_field, min_size, max_size):
    """ Returns a list containing values of the size_field attribute from Graph range 
        normalized between [min_size,max_size] interval.

    Parameters 
    ----------

    G : graph.
        A networkx graph.

    size_field : graph attribute
        graph node attribute containing numbers(integers or floats). 
        See : https://networkx.github.io/documentation/networkx-1.10/tutorial/tutorial.html#adding-attributes-to-graphs-nodes-and-edges for learning about graph attributes

    min_size : float
        minimum value for the new range
    max_size : float
        maximum value for the new range.

    Notes
    --------

    Mapping/scaling a number to a certain range like [0,1] or [-1,1]

    y = (x - min(d))*(max(n)-min(n))
        _____________________________  + min(n)
            (max(d)-min(d))

    min(d) = minimum value in the data

    max(d) = maximum value in the data

    min(n) = minimum value in the new range
    
    max(n) = maximum value in the new range
    input number : x , output : y

    Example 
    -------

    >>>size_field = 'inlink_count'
    >>>node_sizes = set_node_size(G,size_field= "inlink_count",min_size = 0.1, max_size=800)

    Returns
    -------
    list
        list of node sizes normalized to the range.

    """

    try:
        import numpy as np
    except ImportError:
        raise ImportError("Numpy required for calculation")
    vals = np.array([n[1][size_field] for n in G.nodes(data=True)])
    min_val = vals.min()
    max_val = vals.max()
    return (((vals - min_val)*(max_size-min_size))/(max_val-min_val)) + min_size


def filter_graph(G, filter_by=None, top=None):
    """Filters the graph by returning the subgraph for the top x nodes for the given filter_by field.
    
    To learn about subgraphs see : https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.Graph.subgraph.html

    Parameters  
    ----------

    G : graph.
        A networkx graph.

    filter_by : graph node attribute
        Numerical node attribute to filter the graph. 

    top : int
        Number of top nodes to return. 
        E.g if the node attribute is node_size then the function returns top = 100 largest node subgraph.


    Example  
    -------

    >>> filter_field = "inlink_count"
    >>> filter_graph(G,filter_by=filter_field,top=k)

    Returns
    -------
    nx.Graph
        Subgraph after filtering by the node attribute.
    """
    if top <= len(G.nodes()):
        filter = {n[0]: n[1][filter_by] for n in G.nodes(data=True)}
        filter_nodes = sorted(
            filter.items(), key=lambda x: x[1], reverse=True)[0:top]
        return G.subgraph([n[0] for n in filter_nodes])
    else:
        raise ValueError(
            "Subgraph can't contain more nodes than original graph")


def set_node_label(G, label_field):
    """ Returns a dict mapping nodes to the labels. 
    
    Helper function for use in visualization functions like nx.draw_networkx_labels.

    Parameters 
    ----------

    G : graph.
        A networkx graph.

    label_field : node attribute
        Node attribute to be set as a the label for the node.

    Example
    -------

    >>> label_field = "label"
    >>> labels = set_node_label(G,label_field)

    Returns
    -------
    list
        List of node labels

    """
    node_labels = dict((n[0], n[1][label_field]) for n in G.nodes(data=True))
    return node_labels


def edgecolor_by_source(G, node_colors):
    """ Returns a list of colors to set as edge colors based on the source node for each edge.

    Parameters 
    ----------

    G : graph.
        A networkx graph.

    node_colors : list 
        List of node colors.

    Example  
    --------

    >>> colormap = {'male':'b','female':'r'}
    >>> node_colors = set_node_color(G,"gender",colormap)
    >>> edge_colors = edgecolor_by_source(G,node_colors)

    Returns
    -------
    list
        list of colors for each edge of the graph color set by the source node.

    """

    edge_colormap = []
    node_colormap = dict(zip(G.nodes(), node_colors))
    for edge in G.edges():
        edge_colormap.append(node_colormap[edge[0]])
    return edge_colormap


def get_subgraph_pos(G, pos):
    """ Returns the filtered positions for subgraph G. If subgraph = original graph then pos will be returned.

    Parameters 
    ----------

    G : nx.Graph
        A graph object.
    Pos : dict
        A dictionary with nodes as keys and positions as values.

    Example 
    -------

    >>> pos  = nx.spring_layout(G)
    >>> subgraph_nodes = ['1','2','3']
    >>> subgraph = G.subgraph(subgraph_nodes)
    >>> subgraph_positions = get_subgraph_pos(subgraph,pos)

    Returns
    -------
    dict 
        Assuming positions were generated earlier for a larger graph with some layout algorithm
        this functions returns the filtered positions by the subgraph. 

    """
    return {k: v for k, v in pos.items() if k in G.nodes()}


def draw_networkx_nodes_custom(G, pos, node_size, node_color='r', alpha=1, ax=None, **kwargs):
    """Draws networkx graph nodes with circles instead of using plt.scatter function like draw_networkx_nodes

    Parameters
    ----------

    G : nx.Graph
        A networkx graph object.
    pos : dict
        A dictionary with nodes as keys and positions as values.
    node_size : list
        A list containing node sizes for each node.
    node_color : str or list 
        A single color or list containing color values. Behavior same as draw_networkx_nodes
    alpha : float
        opacity (between 0-1) for setting transparency of the nodes
    ax : axis 


    """
    try:
        import matplotlib
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("Matplotlib required for draw()")
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    x = [v[0] for v in pos.values()]
    y = [v[1] for v in pos.values()]

    patches = [plt.Circle((x, y), radius=s)
               for x, y, s in zip(x, y, node_size)]

    coll = matplotlib.collections.PatchCollection(
        patches, color=node_color, alpha=alpha, **kwargs)
    ax.add_collection(coll)

    # ax.margins(0.01)


# https://stackoverflow.com/questions/32444037/how-can-i-plot-many-thousands-of-circles-quickly
