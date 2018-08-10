
import numpy as np
import pytest
from mediaviz.rotation import rotation_layout

def test_rotation_layout():
    # make fake pos dictionary with known points
    pos = {'1':(1,1),'2':(1,0)}
    result = rotation_layout(pos,180,origin=(0,0))
    expected_result_vals = [[-1,-1],[-1,0]]
    result_vals = np.round(list(result.values()))
    # assert that rotation layout returns a dictionary again
    assert type(pos) == type(result)
    # assert that expected values for the positions matches the resulting values
    assert np.all(expected_result_vals == result_vals)

