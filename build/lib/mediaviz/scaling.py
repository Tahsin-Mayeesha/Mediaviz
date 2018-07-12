# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 20:25:32 2018

@author: USER
"""

import math
from itertools import combinations

def get_distance(pos1,pos2):
    """ Returns distance between two points
    
    Params : 
    
    pos1 : tuple in (x,y) format
    pos2 : tuple in (x,y) format
    
    """
    return math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)

    

def get_pairwise_distance_between_largest_nodes(G,pos,node_sizes,k=20):
    """ 
    Boolean. Returns the distances between top k largest nodes
    Parameters : 
    ____________
    
    G : A graph object
    pos : dict containing the position of the nodes
    k : number of nodes to consider    
    """
    top_k_nodes = [n[0] for n in sorted(node_sizes.items(),key=lambda x:x[1], reverse = True)[0:k]]
    top_k_pos = {k:v for k,v in pos.items() if k in top_k_nodes}
    distances = {}
    for n1,n2 in combinations(top_k_nodes,2):
        distances[(n1,n2)]=get_distance(pos[n1],pos[n2])
            
    return distances


def direct_scaling_ratio(G,pos,node_sizes,ideal_distance = 450,k=20):
    """ Returns the ratio of the ideal vs current top node distance """
    result = get_pairwise_distance_between_largest_nodes(G,pos,node_sizes,k=20)
    current_minimum_top_node_distance = min(result.values())
    nodes = min(result,key=result.get)
    ideal_minimum_top_node_distance = node_sizes[nodes[0]] + node_sizes[nodes[1]] + 50
    return ideal_minimum_top_node_distance/current_minimum_top_node_distance
    #return ideal_distance/current_minimum_top_node_distance
    

def scale_layout(pos,scale):
    
    """ Scales layout """
    
    return { k:(v[0]*scale,v[1]*scale) for k,v in pos.items()}
