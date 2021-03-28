import networkx as nx
nx.__version__
'2.2rc1.dev_20180521153746'
import numpy as np
import matplotlib.pyplot as plt
from functions import rand_graph_generator, label_prop
import time
from community import community_louvain
from networkx.algorithms.community.quality import coverage, performance, modularity
import random
from networkx.generators.community import LFR_benchmark_graph


random.seed(10)
# cluster_size = 100
# nb_clusters = 4
# p_list = [0.16, 0.05, 0.1]
# q_list = [0.04, 0.15, 0.1]
# for p,q in zip(p_list, q_list):
# 	G = rand_graph_generator(cluster_size, nb_clusters, p, q)

# 	##--------------------- print for label propagation result
# 	G_treated = label_prop(G, max_iter = 100)
# 	labels = [G_treated.nodes[node]["label"] for node in G_treated.nodes]
# 	# print(labels)
# 	labels = list(set(labels))
# 	partitions = []
# 	for label in labels:
# 		partitions.append(set([node for node in G_treated.nodes if G_treated.nodes[node]["label"] == label]))
# 	# start = time.time()
# 	print('modularity, coverage, performance : ', modularity(G_treated, partitions), 
# 		coverage(G_treated, partitions), performance(G_treated, partitions))
# 	# end = time.time()
# 	# print(end-start)



# 	##--------------------- print for louvain result
# 	# start = time.time()
# 	partition = community_louvain.best_partition(G)
# 	# print(partition)
# 	labels = [partition[node] for node in G.nodes]
# 	labels = list(set(labels))
# 	partitions = []
# 	for label in labels:
# 		partitions.append(set([node for node in G.nodes if partition[node] == label]))
# 	# print(modularity(partitions, G))
# 	# end = time.time()
# 	print('modularity, coverage, performance : ', modularity(G, partitions), 
# 		coverage(G, partitions), performance(G, partitions))
# 	# # print(end-start)


n = 400 ## numbe nodes in th created graph
tau1 = 3
tau2 = 1.5
mu = 0.75
G = LFR_benchmark_graph(n, tau1, tau2, mu, average_degree=5, min_community=100, seed=10)
print('ok')
#--------------------- print for label propagation result
G_treated = label_prop(G, max_iter = 100)
labels = [G_treated.nodes[node]["label"] for node in G_treated.nodes]
# print(labels)
labels = list(set(labels))
partitions = []
for label in labels:
	partitions.append(set([node for node in G_treated.nodes if G_treated.nodes[node]["label"] == label]))
# start = time.time()
print('modularity, coverage, performance : ', modularity(G_treated, partitions), 
	coverage(G_treated, partitions), performance(G_treated, partitions))
# end = time.time()
# print(end-start)

##--------------------- print for louvain result
# start = time.time()
partition = community_louvain.best_partition(G)
# print(partition)
labels = [partition[node] for node in G.nodes]
labels = list(set(labels))
partitions = []
for label in labels:
	partitions.append(set([node for node in G.nodes if partition[node] == label]))
# print(modularity(partitions, G))
# end = time.time()
print('modularity, coverage, performance : ', modularity(G, partitions), 
	coverage(G, partitions), performance(G, partitions))
# # print(end-start