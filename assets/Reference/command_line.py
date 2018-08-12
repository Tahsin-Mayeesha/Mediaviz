import warnings
warnings.filterwarnings('ignore')
import networkx as nx
import sys
from mediaviz.draw import draw_forceatlas2_network
from mediaviz.viz_parser import parse_colors, parse_size

def main():
    if len(sys.argv) < 2:
        sys.exit('usage: %s < input gexf' % sys.argv[0])

    # Input Graph file 

    infile = sys.argv[1]
    print(infile)

    G = nx.read_gexf(infile)
    node_colors = list(parse_colors(infile,hex=True).values())
    draw_forceatlas2_network(
        G,
        num_labels = 20,
        node_colors = node_colors,
        with_labels=True, label_field="label",
        filter_by="inlink_count", top=100,
        size_field = "inlink_count",min_size=0.1,max_size=200,
        adjust_labels=True,
        node_opacity=0.5, edge_opacity=0.01,
        font_size=8,
        filename= "network_viz.png", title=infile,
        edge_color_by_source=True,
        figsize=(10, 10))


    

    
main()