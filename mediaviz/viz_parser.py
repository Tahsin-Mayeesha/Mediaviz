from xml.etree.cElementTree import Element, ElementTree, SubElement, tostring
import matplotlib.colors as colors

def convert_rgb_to_hex(color_code):
    rgb_color_code = color_code['r'],color_code['g'],color_code['b']
    hex_code = colors.rgb2hex([(1.0*float(x))/255 for x in rgb_color_code])
    return hex_code
    


def parse_colors(path,hex=False):
    tree = ElementTree(file=path)
    root = tree.getroot()
    nodes = root.findall('./{http://www.gexf.net/1.2draft}graph/{http://www.gexf.net/1.2draft}nodes/')
    color_codes = {}
    for node in nodes:
        id = node.attrib['id']
        color_code = node.findall('./{http://www.gexf.net/1.1draft/viz}color')[0].attrib
        if hex:
            hex_code = convert_rgb_to_hex(color_code)
            color_codes[id] = hex_code
        else:
            color_codes[id]=color_code
        
    return color_codes



def parse_size(path):
    tree = ElementTree(file=path)
    root = tree.getroot()
    nodes = root.findall('./{http://www.gexf.net/1.2draft}graph/{http://www.gexf.net/1.2draft}nodes/')
    sizes = {}
    for node in nodes:
        id = node.attrib['id']
        size = node.findall('./{http://www.gexf.net/1.1draft/viz}size')[0].attrib
        sizes[id]=int(size['value'])
    return sizes




def parse_position(path):
    tree = ElementTree(file=path)
    root = tree.getroot()
    nodes = root.findall('./{http://www.gexf.net/1.2draft}graph/{http://www.gexf.net/1.2draft}nodes/')
    positions = {}
    for node in nodes:
        id = node.attrib['id']
        position = node.findall('./{http://www.gexf.net/1.1draft/viz}position')[0].attrib
        positions[id]= (position['x'],position['y'])
    return positions