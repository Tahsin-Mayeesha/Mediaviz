import numpy as np



def set_node_color(G,color_by,colormap=None):
    node_colors = [colormap[n[1][color_by]] for n in G.nodes(data=True)]
    return node_colors


def set_node_size(G,size_field,min_size,max_size):
    """ https://www.youtube.com/watch?v=SrjX2cjM3Es """
    import numpy as np
    
    vals = np.array([n[1][size_field] for n in G.nodes(data=True)])
    min_val = vals.min()
    max_val = vals.max()
    return (((vals - min_val)*(max_size-min_size))/(max_val-min_val)) + min_size
        

    



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

def rotate(point, angle, origin = (0,0)):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point
    angle = math.radians(angle)

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

# rotation example  : pos2 = {k:rotate(v,45,(0.5,0.5)) for k,v in pos2.items()}


def draw_networkx_nodes_custom(G,pos,node_size=300,node_color='r',alpha = 1, ax=None, **kwds):
    
    
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("Matplotlib required for draw()")
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise
        
    if pos == None:
        pos = nx.drawing.spring_layout(G)  # default to spring layout
        
    if ax == None:
        ax = plt.gca()
        
    
    
    x =[v[0] for v in pos.values()]
    y =[v[1] for v in pos.values()]
    
    patches = [plt.Circle((x,y),radius=s) for x,y,s in zip(x,y,node_size)]
    
    
    coll = matplotlib.collections.PatchCollection(patches,color=node_colors,alpha=alpha,**kwds)
    ax.add_collection(coll)

    ax.margins(0.01)    
    
    
# https://stackoverflow.com/questions/32444037/how-can-i-plot-many-thousands-of-circles-quickly


