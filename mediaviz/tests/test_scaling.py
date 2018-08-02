import pytest
from mediaviz.scaling import *

def test_get_distance():
    # check with random test points
    assert get_distance((0,0),(0,1)) == 1
    assert get_distance((0,0),(0,0)) == 0
    

def test_get_pairwise_distance_between_largest_nodes():
    pass
    # test for node size 0 
    # test for null values

def test_direct_scaling_ratio():
   pass
   # check if it returns a null value or not
    

def test_scale_layout():
   pass
   # check if returned output pos dict is equal length to input
   # check if all values has been scaled
   # check for null values