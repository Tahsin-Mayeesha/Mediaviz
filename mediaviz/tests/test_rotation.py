
import numpy as np
import pytest
from mediaviz.rotation import rotate,rotation_layout

def test_rotate():
    # check with well known points and rotations
    result1 = rotate(point=(1,1),angle=180, origin = (0,0))
    result2 = rotate(point=(1,0),angle=90, origin = (0,0))
    # note : rounding in the function may harm the layout positions from fa2l by reducing precision, so
    # rounding in the test
    assert np.all(np.round(result1)==np.array([-1.,-1.]))
    assert np.all(np.round(result2)==np.array([0.,1.]))
    

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

