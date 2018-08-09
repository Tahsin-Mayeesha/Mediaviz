from xml.etree.cElementTree import Element, ElementTree, SubElement, tostring
import matplotlib.colors as colors

def convert_rgb_to_hex(color_code):
    rgb_color_code = color_code['r'],color_code['g'],color_code['b']
    hex_code = colors.rgb2hex([(1.0*float(x))/255 for x in rgb_color_code])
    return hex_code
    


def parse_colors(path,hex=False):
    tree = ElementTree(file=path)
    root = tree.getroot()
    nodes = [child for child in root.iter() if "nodes" in child.tag ][0]
    color_codes = {}
    for node in nodes:
        id = node.attrib['id']
        color_code = [child for child in node if "color" in child.tag][0].attrib
        if hex:
            hex_code = convert_rgb_to_hex(color_code)
            color_codes[id] = hex_code
        else:
            color_codes[id]=color_code
        
    return color_codes



def parse_size(path):
    tree = ElementTree(file=path)
    root = tree.getroot()
    nodes = [child for child in root.iter() if "nodes" in child.tag ][0]
    sizes = {}
    for node in nodes:
        id = node.attrib['id']
        size = [child for child in node if "size" in child.tag][0].attrib
        sizes[id]=float(size['value'])
    return sizes




def parse_position(path):
    tree = ElementTree(file=path)
    root = tree.getroot()
    nodes = [child for child in root.iter() if "nodes" in child.tag ][0]
    positions = {}
    for node in nodes:
        id = node.attrib['id']
        position = [child for child in node if "position" in child.tag][0].attrib
        positions[id]= (float(position['x']),float(position['y']))
    return positions