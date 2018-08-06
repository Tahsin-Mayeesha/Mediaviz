def rotate(point, angle, origin = (0,0)):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians. Helper function for rotating a layout.
    
    Parameters : 
    ____________
    
    point : tuple in (x,y) form
    angle : angle in degrees
    origin : point will rotate with respect to the origin.
    
    """
    import math
    ox, oy = origin
    px, py = point
    angle = math.radians(angle)
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

# rotation example  : pos2 = {k:rotate(v,45,(0.5,0.5)) for k,v in pos2.items()}

def rotation_layout(pos,angle,origin=(0,0)):
    
    """ Rotates the pos to the given angle with respect to origin.
    
    Parameters : 
    ____________
    
    pos : A dictionary with nodes as keys and positions as values.
    
    angle : angle in radians
    
    origin : point will rotate with respect to the origin.

    
    
    """
    return { k:rotate(v,angle,origin) for k,v in pos.items()}