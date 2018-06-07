



def set_node_color(G,color_by,colormap=None):
    node_colors = [colormap[n[1][color_by]] for n in G.nodes(data=True)]
    return node_colors


def set_node_size(G,size_field,max_node_size,dict_form=False):
    max_node_val = max([n[1][size_field] for n in G.nodes(data=True)])
    node_sizes = [max_node_size * (n[1][size_field] / max_node_val) for n in G.nodes(data=True)]
    return node_sizes
    



def filter_graph(G,filter_by=None,top=None):
    filter = {n[0]:n[1][filter_by] for n in G.nodes(data=True)}
    filter_nodes = sorted(filter.items(), key=lambda x: x[1],reverse=True)[0:top]
    return G.subgraph([n[0] for n in filter_nodes])

def set_node_label(G,label):
    node_labels = dict((n[0], n[1][label]) for n in G.nodes(data=True))
    return node_labels

def edgecolor_by_source(G,node_colors):
    edge_colormap = []
    node_colormap = dict(zip(G.nodes(),node_colors))
    for edge in G.edges():
        edge_colormap.append(node_colormap[edge[0]])
    return edge_colormap

    
    
def get_subgraph_pos(G,pos):
    return {k:v for k,v in pos.items() if k in G.nodes()}