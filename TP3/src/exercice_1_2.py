from PageRank import poweriteration

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import scipy.sparse as sprs

n = 2070486

# Loading graph

nodes = np.load('../data/nodes.npy',allow_pickle='TRUE').item()
in_degree = np.load('../data/in_degree.npy',allow_pickle='TRUE').item()
out_degree = np.load('../data/out_degree.npy',allow_pickle='TRUE').item()
Page_ids = np.load('../data/Page_ids.npy',allow_pickle='TRUE').item()
matrix = sprs.load_npz('../data/matrix.npz')

# PageRank

P = poweriteration(n,matrix,0.15)

# Highest and Lowest Values

nodes = {i:v for v,i in nodes.items()}
ranks, sorted_node = zip(*sorted([(x,nodes[i]) for (i,x) in enumerate(P)]))
nodes = {i:v for v,i in nodes.items()}

highest = sorted_node[-5:]
lowest = sorted_node[:5]
highest = [Page_ids[i] for i in highest]
lowest = [Page_ids[i] for i in lowest]

print("\nThe 5 pages with the highest PageRank are :", highest)
print(ranks[-5:])
print("\nThe 5 pages with the lowest PageRank are :", lowest)
print(ranks[:5])
# Plots

P1 = poweriteration(n,matrix,0.1)
P2 = poweriteration(n,matrix,0.2)
P3 = poweriteration(n,matrix,0.5)
P4 = poweriteration(n,matrix,0.9)


print("\nplot1")
plt.figure()
plt.grid(True)
plt.scatter(ranks,[in_degree[k] for k in sorted_node],s=1,c='b')
plt.xscale('log')
plt.yscale('log')
plt.ylim(1,1e6)
plt.xlabel('PageRank with alpha = 0.15')
plt.ylabel('in_degree')
plt.savefig('../res/plot1.png')

print("\nplot2")
plt.figure()
plt.grid(True)
plt.scatter(ranks,[out_degree[k] for k in sorted_node],s=1,c='b')
plt.xscale('log')
plt.yscale('log')
plt.ylim(1,1e4)
plt.xlabel('PageRank with alpha = 0.15')
plt.ylabel('out_degree')
plt.savefig('../res/plot2.png')

print("\nplot3")
plt.figure()
plt.grid(True)
plt.scatter(ranks,[P1[nodes[k]] for k in sorted_node],s=1,c='b')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('PageRank with alpha = 0.15')
plt.ylabel('PageRank with alpha = 0.1')
plt.savefig('../res/plot3.png')

print("\nplot4")
plt.figure()
plt.grid(True)
plt.scatter(ranks,[P2[nodes[k]] for k in sorted_node],s=1,c='b')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('PageRank with alpha = 0.15')
plt.ylabel('PageRank with alpha = 0.2')
plt.savefig('../res/plot4.png')

print("\nplot5")
plt.figure()
plt.grid(True)
plt.scatter(ranks,[P3[nodes[k]] for k in sorted_node],s=1,c='b')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('PageRank with alpha = 0.15')
plt.ylabel('PageRank with alpha = 0.5')
plt.savefig('../res/plot5.png')

print("\nplot6")
plt.figure()
plt.grid(True)
plt.scatter(ranks,[P4[nodes[k]] for k in sorted_node],s=1,c='b')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('PageRank with alpha = 0.15')
plt.ylabel('PageRank with alpha = 0.9')
plt.savefig('../res/plot6.png')