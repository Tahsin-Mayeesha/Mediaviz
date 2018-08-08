# Mediaviz

This repository is for my project [Automating Network Visualization and community detection of Media Sources Network from Mediacloud data.](https://summerofcode.withgoogle.com/projects/#6265196406898688)  with Google Summer Of Code 2018. The goal is to create network visualizations with force atlas 2 layout and appropriate visual aesthetics on top of python's popular network analysis library networkx. 

See blog posts related to the project in the following links.

- [GSOC 2018 Experience : Visualizing Media Data With Network Analysis (PART 1 )](https://medium.com/learning-machine-learning/gsoc-2018-experience-visualizing-media-data-with-network-analysis-part-1-c4ba4b76b1aa)
- [GSOC 2018 : Network Visualization Of MediaCloud Topic Network + 1st evaluation (Part 2)](https://medium.com/learning-machine-learning/gsoc-2018-network-visualization-of-mediacloud-topic-network-1st-evaluation-part-2-ca72e25a88d5)

![Deep State Network](assets/deep_state.png)





# Installation





# Dependencies : 

* [networkx](https://networkx.github.io)

* [fa2l](https://github.com/bosiakov/fa2l/tree/master/fa2l)

* [adjusttext](http://adjusttext.readthedocs.io)

* [matplotlib](https://matplotlib.org)

* [numpy](http://www.numpy.org/)


# Usage

* Draw a Network with Force Atlas 2 Layout With Default Parameters

```python
import networkx as nx
import os
from mediaviz.visualize import draw_forceatlas2_network

fname = os.path.join(os.path.dirname(__file__), 'graphname.gexf')
G = nx.read_gexf(fname)

draw_forceatlas2_network(G)
```



* Drawing Network with Force Atlas 2 Layout with customized colormap, node size and labels
* Drawing Network With Community Detection and Coloring

```python
import community
import networkx as nx
from mediaviz.community_utils import get_community_graph, get_community_colormap
from mediaviz.draw import draw_forceatlas2_network

G = nx.florentine_families_graph() 
# get the community partitions and set partition as an attribute for the nodes 
G, partitions = get_community_graph(G) 
# colormaps are automatically assigned for each partition as randomly genererated hex colors
colormap = get_community_colormap(partitions)
# use the draw function as usual with forceatlas2 layout as default
draw_forceatlas2_network(
        G,
        color_by="partition", colormap=colormap,
        node_sizes = 10,
        with_labels=True, 
        edge_color_by_source=True, node_opacity = 1, edge_opacity = 1,
        font_size=10, filename = "community.png",
        figsize=(10, 10));
```

![ ](assets/community.png)

* Only Using Draw Function for Customized Visualization With Other Layout Algorithms

```python
import networkx as nx
from mediaviz.draw import draw_forceatlas2_network
G = nx.karate_club_graph()
pos = nx.spring_layout(G)
draw_forceatlas2_network(G,
                         pos = pos,
                         node_sizes=10,
                         color_by="club",
                         colormap={"Officer":"r","Mr. Hi":"b"},
                         node_opacity=1,edge_opacity=1, filename="karate_club.png",
                         edge_color="lightgray")
```

![](assets/karate_club.png)

# Documentation

* Core Drawing Functions
* Utilities 









