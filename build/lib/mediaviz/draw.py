import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fa2l import force_atlas2_layout
from adjustText import adjust_text
import networkx as nx

from .utils import set_node_size, set_node_color, set_node_label
from .utils import edgecolor_by_source, filter_graph, get_subgraph_pos
from .utils import draw_networkx_nodes_custom
from .scaling import get_auto_scale, scale_layout

def draw_forceatlas2_network(
        G,
        pos=None, fa2l_iterations = 50, fa2l_scaling_ratio = 38,
        scale = "auto",
        num_labels=None,
        node_list = None,
        node_color='red', color_by=None, colormap=None, 
        node_size=10,
        size_field=None, min_size=0.1, max_size=100,
        with_labels=False, label_field=None,
        filter_by=None, top=None,
        adjust_labels=True,
        node_opacity=1, edge_opacity=0.05,
        font_size=8, font_color='k', font_family='sans-serif',
        filename="untitled.png", title=None,
        edge_color="lightgray",
        edge_color_by_source=False,
        figsize=(10, 10), fig_dpi=100,
        **kwargs):
    
    if node_list:
        G = nx.subgraph(node_list)
    
    
    if type(G) == nx.DiGraph:
        G = max(nx.weakly_connected_component_subgraphs(G), key=len).to_undirected()

    


    if pos is None:        
        pos = force_atlas2_layout(
        G,
        iterations=fa2l_iterations,
        pos_list=None,
        node_masses=None,
        outbound_attraction_distribution=False,
        lin_log_mode=False,
        prevent_overlapping=False,
        edge_weight_influence=1.0,
        jitter_tolerance=1.0,
        barnes_hut_optimize=True,
        barnes_hut_theta=1.0,
        scaling_ratio=fa2l_scaling_ratio,
        strong_gravity_mode=False,
        multithread=False,
        gravity=1.0)
        
    if scale == "auto":
        if size_field:
            original_node_sizes = dict(zip(G.nodes(), set_node_size(G, size_field=size_field, min_size=min_size, max_size=max_size)))
        elif type(node_size) == int or type(node_size) == float:
            original_node_sizes = dict(zip(G.nodes(),[node_size]*len(G.nodes())))
        else:
            original_node_sizes = dict(zip(G.nodes(),node_size))
        scale = get_auto_scale(G,pos, original_node_sizes, k=20)
        print("scale is " + str(scale))
        pos = scale_layout(pos,scale)
    elif scale:
        pos = scale_layout(pos,scale)
        
    
    if with_labels is True and num_labels is None:
        num_labels = len(G.nodes())

    if filter_by:
        G = filter_graph(G, filter_by=filter_by, top=top)
        pos = get_subgraph_pos(G, pos)

    if color_by:
        node_color = set_node_color(G, color_by=color_by, colormap=colormap)

    if size_field:
        node_size = set_node_size(
            G, size_field=size_field, min_size=min_size, max_size=max_size)
    elif type(node_size) == int or type(node_size) == float:
        node_size = [node_size]*len(G.nodes())
        
    if edge_color_by_source:
        edge_color = edgecolor_by_source(G, node_color)

    if with_labels and label_field:
        node_labels = set_node_label(G, label_field=label_field)
        subset_label_nodes = sorted(zip(G.nodes(), node_size),
                                    key=lambda x: x[1],
                                    reverse=True)[0:num_labels]
        subset_labels = {n[0]: node_labels[n[0]] for n in subset_label_nodes}
        
    if with_labels and label_field is None:
        subset_labels = dict((n, n) for n in G.nodes())


    # plot the visualization

    fig = plt.figure(figsize=figsize,dpi=fig_dpi, **kwargs)
    ax = fig.add_subplot(111)

    # Draw the nodes, edges, labels separately

    draw_networkx_nodes_custom(G,
                               pos=pos, node_size=node_size,
                               node_color=node_color,
                               ax=ax,
                               alpha=node_opacity,
                               **kwargs)
    plt.axis("scaled")
    nx.draw_networkx_edges(
        G, pos=pos, edge_color=edge_color, alpha=edge_opacity, **kwargs)

    if with_labels:
        labels = nx.draw_networkx_labels(
            G, pos=pos, labels=subset_labels, font_size=font_size, 
            font_color=font_color, font_family=font_family,**kwargs)
        if adjust_labels:
            # Adjust label overlapping
            x_pos = [v[0] for k, v in pos.items()]
            y_pos = [v[1] for k, v in pos.items()]
            adjust_text(
                texts=list(labels.values()),
                x=x_pos,
                y=y_pos)
        

    # add title
    if title:
        plt.title(title)

    ax.axis("off")
    # save the plot

    plt.savefig(filename)

    # Show the plot
    plt.show()
