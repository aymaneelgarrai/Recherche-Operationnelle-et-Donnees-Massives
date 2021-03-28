import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

import time
from functions import rand_graph_generator, label_prop
import random

from collections import Counter
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.algorithms.community.quality import coverage, performance, modularity
from networkx.drawing.nx_pylab import draw

random.seed(10)


cluster_size = 100
nb_clusters = 4
p = 0.15
q = 0.005
G = rand_graph_generator(cluster_size, nb_clusters, p, q)
G_treated = label_prop(G, max_iter = 100)

print(Counter([G_treated.nodes[node]['label'] for node in G_treated.nodes]))

# labels = [G_treated.nodes[node]['label'] for node in G_treated.nodes] ## get the labels
# fig = plt.figure()
# draw(G_treated,node_color=labels,cmap='jet')
# fig.savefig("label_15_01.png")
