import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from collections import Counter
import operator
import random


def rand_graph_generator(cluster_size = 100, nb_clusters = 4, p = 0.1, q = 0.01):
	'''
	Generate a random graph with several clusters of equal size such that :
		- Each pair of nodes in the same cluster is connected with a probability p
		- Each pair of nodes in different clusters is connected with a probability q<= p

	'''
	G = nx.Graph()
	num_nodes = cluster_size*nb_clusters
	## Add nodes and give them lables
	label = 0
	for j in range(num_nodes):
		G.add_node(j)
		G.nodes[j]['label'] = label
		if (j+1)%(cluster_size)==0:
			label+=1
    ## Randomly Create edges between veteces 
	for i in range(num_nodes):
		for j in range(i+1, num_nodes):
			x = np.random.uniform()
			if G.nodes[i]["label"] == G.nodes[j]["label"] and x<p:
				G.add_edge(i,j)
			elif G.nodes[i]["label"] != G.nodes[j]["label"] and x<q:
				G.add_edge(i,j)
	return G


def label_prop(graph, max_iter = 100):
    ## Save copy of the input graph
    G = graph.copy()
    # Create unique label for every node
    labels = [*range(len(G))]
    random.shuffle(labels)
    for i, node in enumerate(G.nodes):
        G.nodes[node]["label"] = labels[i]
    ## Save list of nodes to avoid confusion after nodes rearrangement
    nodes = [node for node in G.nodes]
    ite = 0
    stop_condition = 0
    while ite <max_iter and stop_condition == 0:
        ## Shuffle nodes randomly 
        node_mapping = dict(zip(G.nodes(), sorted(G.nodes(), key=lambda k: random.random())))
        G = nx.relabel_nodes(G, node_mapping)
        stop_condition = 1
        for node in nodes:
        	## Get the labels of each neighbor for the current node
            neighbors_lables = [G.nodes[neighbor]['label'] for neighbor in G.neighbors(node)]
            ## Get occurences of each label amoung the neighbors
            neighbors_lables_occurences = dict(Counter(neighbors_lables))
            ## Check if the current node actually have neighbors
            if len(neighbors_lables_occurences) >0:
                new_label = sorted(neighbors_lables_occurences, key=neighbors_lables_occurences.get, reverse=True)[0]
                if G.nodes[node]['label'] != new_label :
                    stop_condition = 0
                G.nodes[node]['label'] = new_label
            else:
                stop_condition = 0

        ite +=1
    print(ite)
    return G

