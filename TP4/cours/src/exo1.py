import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from Exo1 import rand_graph_generator, label_prop

from networkx.drawing.nx_agraph import graphviz_layout
from networkx.algorithms.community.quality import coverage, performance, modularity

cluster_size = 100
nb_clusters = 4
p = 0.16
q = 0.04
G_treated = rand_graph_generator(cluster_size, nb_clusters, p, q)
# G_treated = label_prop(G, max_iter = 100)

fig = plt.figure(figsize=(15, 15))

pos=nx.spring_layout(G_treated)
nx.draw_networkx_nodes(G_treated, pos, nodelist=[node for node in G_treated.nodes if G_treated.nodes[node]['label']==0], node_color='r', node_size=10, alpha=0.8)
nx.draw_networkx_nodes(G_treated, pos, nodelist=[node for node in G_treated.nodes if G_treated.nodes[node]['label']==1], node_color='b', node_size=10, alpha=0.8)
nx.draw_networkx_nodes(G_treated, pos, nodelist=[node for node in G_treated.nodes if G_treated.nodes[node]['label'] ==2], node_color='g', node_size=10, alpha=0.8)
nx.draw_networkx_nodes(G_treated, pos, nodelist=[node for node in G_treated.nodes if G_treated.nodes[node]['label']==3], node_color='c', node_size=10, alpha=0.8)

nx.draw_networkx_edges(G_treated, pos, edgelist=[edge for edge in G_treated.edges], width=1, alpha=0.5, edge_color = 'y')
nx.draw_networkx_edges(G_treated, pos, edgelist=[edge for edge in G_treated.edges], width=1, alpha=0.5, edge_color = 'k')

fname = "label_15_01.png"
plt.axis('off')
plt.savefig(fname, dpi=1200, format="png",
        transparent=True, bbox_inches="tight", pad_inches=0.1)
