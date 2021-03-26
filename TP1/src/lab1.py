import numpy as np
from numba import jit
from collections import deque
import time
from scipy.sparse import dok_matrix, lil_matrix
from tqdm import tqdm
import random

available_graphs = {'amazon', 'lj','orkut'}

####################################################################################################
# Answer to exercice 1 
# Creating a program to count the number of nddes and edges in a graph and 
# writes this value in the standard output 
####################################################################################################

def nb_nodes_edges(graph):

    # Preparing the file
    to_count = "../data/com-"+graph+".ungraph.txt"
    fp = open(to_count)

    # Target variables
    nb_edges = 0 #integer
    nodes = set() #set (to make it easier note counting nodes multiple times)

    for i, line in enumerate(fp):
        # We skip the first four lines 
        if i>=4 :
            # We add an edge
            nb_edges += 1
            # We get the starting and finishing nodes
            from_node, to_node = map(int, line.split())
            # We add the nodes to a set of nodes
            nodes.add(from_node)
            nodes.add(to_node)
    fp.close()
    return len(nodes), nb_edges
    
####################################################################################################
# Answer to exercice 2 :
####################################################################################################

availabe_formats = {'list_edges', 'adj_matrix', 'adj_array'}

def load_graph(graph, graph_format):

    # Preparing the file
    to_count = "../data/com-"+graph+".ungraph.txt"
    fp = open(to_count)

    # If we want a format as list of edges
    if graph_format == 'list_edges':

        # Initialize the list of edges
        list_edges = []
        
        # Go through the file 
        for i, line in enumerate(fp):

            # Skip the first four lines
            if i>=4 :

                # Add the edge 
                from_node, to_node = map(int, line.split())
                list_edges.append((from_node, to_node))
                list_edges.append((to_node, from_node))
        return list_edges
    
    # If we want an adjacency matrix 
    if graph_format == 'adj_matrix':
        nb_nodes = {"amazon":334863, "lj":3997962, "orkut":3072441}
        n = nb_nodes[graph]

        # As a sparse matrix
        adj_matrix = lil_matrix((n,n))
    
        # Reindexation of the elements 
        reindex = {}
        i=0

        # Go through the file
        for line in fp:

            if not(line.startswith("#")) :

                from_node, to_node = map(int, line.split())

                if from_node not in reindex.keys():
                    reindex[from_node] = i
                    i += 1
                if to_node not in reindex.keys():
                    reindex[to_node] = i
                    i += 1

                # Add an element in the adjacency matrix
                adj_matrix[reindex[from_node], reindex[to_node]] = 1

        fp.close()
        adj_matrix = adj_matrix.tocsr()
        adj_matrix = adj_matrix.transpose() + adj_matrix 
        # Return the adjacency matrix
        return adj_matrix
    
    # If we want an adjacency array
    if graph_format == 'adj_array':
        
        # Coding the array as a dictionnary 
        adj_array = dict()

        # Go through the file
        for i, line in enumerate(fp):
            if i>=4 :

                from_node, to_node = map(int, line.split())
                
                # Build the array
                adj_array.setdefault(from_node, [])
                adj_array[from_node].append(to_node)
                adj_array.setdefault(to_node,[])
                adj_array[to_node].append(from_node)
        
        return adj_array
    fp.close()

####################################################################################################
# Answer to exercice 3 :
####################################################################################################

# For this the graphs will be encoded as adjacency array 
# The BFS will go through the graph and compute the node with the maximum distance from the start
def BFS(graph,start):
    # Create FIFO
    queue = deque()

    # Add the start to the FIFO
    queue.append(start)
    # We mark the start
    visited = dict()
    visited[start] = 0
    u = start
    
    # While FIFO not empty do
    while queue:
        w = u
        # Pop element 
        u = queue.popleft()
        
        m = visited[u] 
        
        # For each v neighbour of u
        for v in graph[u]:

            # If the node has node been checked 
            if not v in visited:

                # Add v 
                queue.append(v)
                # Mark it 
                visited.setdefault(v,m+1)
                

    return visited, u, w


def lower_bound_estimate(graph,start):
    distances = []
    alpha = 10
    while alpha >= 0:
        mark, start, _ = BFS(graph, start)

        distances.append(mark[start])
        alpha -= 1
    return max(distances)
  

def upper_bound_estimate(graph, s):
    mark, s, prev = BFS(graph, s)
    return mark[s] + mark[prev]


####################################################################################################
# Answer to exercice 4 :
####################################################################################################

# Non efficient way 
def count_triangles(graph):    
    # Number of triangles 
    res = 0

    for u in graph:

        neighbors = list(set(graph[u]))

        for v in neighbors :
            
            intersect = list(filter(set(neighbors).__contains__, graph[v]))
            
            res += len(intersect)

    return res//6

# Efficient way
def count_triangles_efficient(graph):

    ########## We start by resorting the graph according to the order presented in the class
    nodes = list(graph.keys())
    sorted_degrees = np.argsort([len(graph[k]) for k in nodes])
    
    temp_1 = {}
    temp_2 = {}
    i = 0
    for i,_ in enumerate(sorted_degrees):
        temp_1[nodes[sorted_degrees[i]]]=i
        temp_2[i] = nodes[sorted_degrees[i]]
        
    sorted_adj_array = {}
    for new in range(i+1):
        l = []
        for old in graph[temp_2[new]]:
            l.append(temp_1[old])
        l.sort()
        sorted_adj_array[new] = l
    
    ######## We then apply the algorithm for counting the trianges
    
    start = time.time()
    count = 0
    tsl = {}
    # We keep the nodes with higher degrees
    for u in sorted_adj_array:
        tsl[u] = [x for x in sorted_adj_array[u] if x>u]
    
    # We apply our algorithm
    for u in sorted_adj_array:

        neighbors = sorted_adj_array[u]
        u_set = set(tsl[u])

        for v in neighbors:

            intersect = list(filter(u_set.__contains__, tsl[v]))
            
            count += len(intersect)
            
    end = time.time()
    return count//2, end-start

####################################################################################################
# Answers of the report
####################################################################################################

def exo_1():


    print('\n######################\nQuestion 1 : Computation of the numbers of nodes and edges for the various graphs:\n######################\n')

    for graph in available_graphs :
        start_time = time.time()
        nb_nodes, nb_edges = nb_nodes_edges(graph)
        print('The {:s} graph has {:d} nodes and {:d} edges.'.format(graph, nb_nodes, nb_edges))
        end_time = time.time()
        print('It took {:3f} seconds\n'.format(end_time-start_time))

def exo_2():

    print('\n######################\nQuestion 2 : Computation of the graph representations for the various graphs:\n######################\n')

    for graph in available_graphs :
        print('For the {:s} graph :\n'.format(graph))
        for graph_format in availabe_formats:
            start_time = time.time()
            load_graph(graph, graph_format)
            print('Computing the {:s} graph as {:s}.'.format(graph, graph_format))
            end_time = time.time()
            print('It took {:3f} seconds\n'.format(round(end_time-start_time,3)))

def exo_3():

    print('\n######################\nQuestion 3 : Computation of the lower and upper bounds of the diameters of the different graphs:\n######################\n')

    for graph in available_graphs :
        
        print('For the {:s} graph :\n'.format(graph))
        
        graph_format = 'adj_array'
        adj_array = load_graph(graph, graph_format)
        
        ############## Lower Bound
        start_time = time.time()
        
        lb = lower_bound_estimate(adj_array,1)

        end_time = time.time()
        
        print('The lower bound of the diameter of the {:s} graph is {:d}.'.format(graph, lb))
        print('It took {:3f} seconds\n'.format(round(end_time-start_time,3)))
        
        ############## Upper bound
        start_time = time.time()

        ub = upper_bound_estimate(adj_array, 1)

        end_time = time.time()

        print('The upper bound of the diameter of the {:s} graph is {:d}.'.format(graph, ub))
        print('It took {:3f} seconds\n'.format(round(end_time-start_time,3)))


def exo_4():

    print('\n######################\nQuestion 4 : Computation of the number of triangles for the different graphs:\n######################\n')
    
    for graph in available_graphs :
        print('For the {:s} graph :\n'.format(graph))

        graph_format = 'adj_array'

        adj_array = load_graph(graph, graph_format)
        start_time = time.time()

        count_nonefficient = count_triangles(adj_array)
        print('The {:s} graph has {:d}.'.format(graph, count_nonefficient))
        print('It took {:3f} seconds with the non efficient algorithm\n'.format(round(time.time()-start_time,3)))


        count_efficient, duration = count_triangles_efficient(adj_array)
        print('The {:s} graph has {:d}.'.format(graph, count_efficient))
        print('It took {:3f} seconds with the efficient algorithm\n'.format(round(duration,3)))


def main():
    exo_1()
    exo_2()
    exo_3()
    exo_4()


main()



























