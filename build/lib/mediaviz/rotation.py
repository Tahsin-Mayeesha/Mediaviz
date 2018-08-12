def _rotate(point, angle, origin = (0,0),unit = 'degree'):
    """Rotate a point counterclockwise by a given angle around a given origin.

    Angle can be both in radian or degree. Helper function for rotating a layout.

    Parameters
    ----------
    point : tuple 
        position in (x,y) form
    angle : float
        angle to rotate the point
    origin : tuple in (x,y) form
        point will rotate with respect to the origin.
    unit : 'degree'/'radian' to indicate if the angle is in degrees or radians. 
        if given in degrees angle is converted to radians.


    Returns
    -------
    tuple
        rotated point as (x,y) tuple.
    """
    import math
    ox, oy = origin
    px, py = point
    if unit == 'degree':
        angle = math.radians(angle)
    if unit == 'radian':
        angle = angle
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

# rotation example  : pos2 = {k:rotate(v,45,(0.5,0.5)) for k,v in pos2.items()}

def rotation_layout(pos,angle,origin=(0,0),unit="degree"):
    
    """ Rotates the pos to the given angle with respect to origin.
    
    Parameters  
    ----------
    
    pos : dict
        A dictionary with nodes as keys and positions as values.
    
    angle : float
        angle in degree or radian
    
    origin : tuple
        the point will rotate with respect to the origin.
    unit : str
        'degree'/'radian' to indicate if the angle is in degrees or radians.If given in degrees 
        angle is converted to radians.

    Returns
    -------
    dict
        Returns the pos dict with positions rotated by the given angle with respect to the given origin.
    
    """
    return { k:_rotate(v,angle,origin,unit) for k,v in pos.items()}