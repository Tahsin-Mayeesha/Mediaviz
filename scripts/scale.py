import math
import networkx as nx
from itertools import combinations
from utils import set_node_size
from fa2l import force_atlas2_layout


def get_distance(pos1,pos2):
    """ Returns distance between two points"""
    return math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)


def has_node_overlap(pos1,pos2,size):
    """ Boolean. Takes in the position of two nodes and their sizes as input.
        Returns true if the two nodes overlap with each other.
    """
    distance = get_distance(pos1,pos2)
    if distance <= size[0] + size[1] :
        return True
    else:
        return False
    

def top_k_node_overlap(G,pos,node_sizes,k=20):
    """ Boolean. Returns True if any of the top 20 nodes overlap with each other.
    
    params : 
    
    G : networkx Graph object
    Pos : dict of {node1:(x1,y1)...} form calculated by a networkx graph layout algorithm
    node_sizes : dict of {node:size} form (edge case : what to do if all nodes are same size?)
    k : number of nodes to check for overlap
    
    """
    top_k_nodes = [n[0] for n in sorted(node_sizes.items(),key=lambda x:x[1], reverse = True)[0:k]]
    top_k_pos = {k:v for k,v in pos.items() if k in top_k_nodes}
    top_k_sizes = {k:v for k,v in node_sizes.items() if k in top_k_nodes}
    overlap = False
    #overlapping_nodes = []
    for n1,n2 in combinations(top_k_nodes,2):
        if has_node_overlap(top_k_pos[n1],top_k_pos[n2],[top_k_sizes[n1],top_k_sizes[n2]]):
            #overlapping_nodes.append((n1,n2))
            overlap = True
            return overlap
    return overlap
    #return overlapping_nodes,top_k_nodes,top_k_pos,top_k_sizes
    #return overlapping_nodes
    
    
    
def has_node_apart(G,pos,node_sizes,k=2,d=0.9):
    """ Boolean. Returns True if any of the top k nodes are too far away from each other.
        params : 
        G = graph object
        pos = dict containing the position of the nodes
        k = number of nodes to consider
        d = how far distance is too far
    
    """
    top_k_nodes = [n[0] for n in sorted(node_sizes.items(),key=lambda x:x[1], reverse = True)[0:k]]
    top_k_pos = {k:v for k,v in pos.items() if k in top_k_nodes}
    node_too_far = False
    for n1,n2 in combinations(top_k_nodes,2):
        if get_distance(pos[n1],pos[n2]) > d:
            node_too_far = True
            return True
    return node_too_far
    

    
def extract_correct_scale(G, node_sizes,min_scale,max_scale):
    first = min_scale
    last = max_scale
    found = False
    iteration = 0
    
    while first<=last and not found:
    
        scale = (first + last)/2
        print("iteration : " + str(iteration))
        print("current range : " + str((first,last)))
        print("current scale : " + str(scale))

        pos = force_atlas2_layout(
              G,
              iterations=50,
              pos_list=None,
              node_masses=None,
              outbound_attraction_distribution=True,
              lin_log_mode=True,
              prevent_overlapping=True,
              edge_weight_influence=1.0,
              jitter_tolerance=1.0,
              barnes_hut_optimize=True,
              barnes_hut_theta=0.5,
              scaling_ratio=scale,
              strong_gravity_mode=False,
              multithread=False,
              gravity=1.0)
        
        node_overlap = top_k_node_overlap(G,pos,node_sizes)
        node_too_far = has_node_apart(G,pos,node_sizes)
        
        print("node_overlap is " + str(node_overlap))
        print("node_too_far is "+ str(node_too_far))
        
        if node_overlap ==False and node_too_far == False :
            found = True
            return (found,scale,pos)
        else:
            if node_overlap == True:
                first = scale+1
            else:
                last = scale-1
        iteration = iteration + 1 
    return (found)


