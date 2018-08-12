from xml.etree.cElementTree import ElementTree
import matplotlib.colors as colors


def _convert_rgb_to_hex(color_code):
    """Converts dict containing rgb color code to hex color code. 

    Parameters
    ----------
    color_code : dict
        A dictionary containing rgb color code. Example : {'r':0,'g':0,'b':0}
    
    Returns
    -------
    str
        hex code of form '#XXXXXX' 

    """
    rgb_color_code = color_code['r'], color_code['g'], color_code['b']
    hex_code = colors.rgb2hex([(1.0*float(x))/255 for x in rgb_color_code])
    return hex_code


def parse_colors(path, hex=False):
    """ Parses the color attribute from .gexf file viz tag and returns the dict with the node colors.

    Default nx.read_gexf() does not read the attributes from the visualization namespace
    of .gexf files so this function is used to read the color codes. 
    
    To learn more see : https://gephi.org/gexf/format/viz.html 


    Parameters
    ----------
    path : str
        File or filename of the graph in .gexf format.
    hex : bool
        whether to return the color codes in hex format. if False rgb color codes are returned.

    Returns
    -------
    dict
        Returns dict containing the color codes. 
        
        Example : {'1':'#FFFFFF'} or {'1':{'r':0,'g':0,'b':0}}

    """
    tree = ElementTree(file=path)
    root = tree.getroot()
    nodes = [child for child in root.iter() if "nodes" in child.tag][0]
    color_codes = {}
    for node in nodes:
        id = node.attrib['id']
        color_code = [
            child for child in node if "color" in child.tag][0].attrib
        if hex:
            hex_code = _convert_rgb_to_hex(color_code)
            color_codes[id] = hex_code
        else:
            color_codes[id] = color_code

    return color_codes


def parse_size(path):
    """Parses the size attribute from .gexf file viz tag and returns the dict with the node sizes.

    Default nx.read_gexf() does not read attributes from the visualization namespace
    of .gexf files so we use this function to get the node sizes. 
    
    To learn more see : https://gephi.org/gexf/format/viz.html 

    Parameters
    ----------
    path : str
        File or filename of the graph in .gexf format.
    
    Returns
    -------
    dict
        Returns dict containing the node sizes. Example : {'1':52.0} 

    """
    tree = ElementTree(file=path)
    root = tree.getroot()
    nodes = [child for child in root.iter() if "nodes" in child.tag][0]
    sizes = {}
    for node in nodes:
        id = node.attrib['id']
        size = [child for child in node if "size" in child.tag][0].attrib
        sizes[id] = float(size['value'])
    return sizes


def parse_position(path):
    """Parses the position attribute from .gexf file viz tag and returns the dict with the node sizes.

    Default nx.read_gexf() does not read attributes from the visualization namespace
    of .gexf files so we use this function to get the node positions, possibly after using layout 
    algorithms in Gephi. 
    
    To learn more see : https://gephi.org/gexf/format/viz.html 

    Parameters
    ----------
    path : str
        File or filename of the graph in .gexf format.
    
    Returns
    -------
    dict
        Returns dict containing the node positions. Example : {'1':(2.0,3.0)} 


    """
    tree = ElementTree(file=path)
    root = tree.getroot()
    nodes = [child for child in root.iter() if "nodes" in child.tag][0]
    positions = {}
    for node in nodes:
        id = node.attrib['id']
        position = [
            child for child in node if "position" in child.tag][0].attrib
        positions[id] = (float(position['x']), float(position['y']))
    return positions
