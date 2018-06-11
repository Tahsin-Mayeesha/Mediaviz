import sys
import networkx as nx
from utils import set_node_size
from scale import extract_correct_scale
print(nx.__version__)


def main():
    if len(sys.argv) < 2:
        sys.exit('usage: %s < input gexf' % sys.argv[0])

    # Input Graph file 

    infile = sys.argv[1]

    G = nx.read_gexf(infile)
    G = max(nx.weakly_connected_component_subgraphs(G), key=len).to_undirected()
    sizes = dict(zip(G.nodes(),set_node_size(G,"inlink_count",0.01,0.003)))
    result = extract_correct_scale(G,sizes,5,100) # Search for the correct scale between 5 to 200 
    if result[0] == True:
        print("scale = " + str(result[1]))
    else:
        print("Search Failed")
    
    
    
main()