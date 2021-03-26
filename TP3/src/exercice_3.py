from PageRank import personalized_poweriteration
import numpy as np
import scipy.sparse as sprs
import matplotlib.pyplot as plt

n = 2070486

# Loading graph

nodes = np.load('../data/un_nodes.npy',allow_pickle='TRUE').item()
Page_ids = np.load('../data/Page_ids.npy',allow_pickle='TRUE').item()
Page_cat = np.load('../data/Page_cat.npy',allow_pickle='TRUE').item()
Cat_ids = np.load('../data/Cat_ids.npy',allow_pickle='TRUE').item()
Chess_Ids = list(np.load('../data/Chess_Ids.npy',allow_pickle='TRUE'))
Boxing_Ids = list(np.load('../data/Boxing_Ids.npy',allow_pickle='TRUE'))
matrix = sprs.load_npz('../data/un_matrix.npz')

# Magnus Carlsen Rooted Pagerank

Magnus_ID = 442682

P0 = np.zeros((n,1))
P0[nodes[Magnus_ID]]=1

P = personalized_poweriteration(n,matrix,P0,0.15)

# Highest and Lowest
                
nodes = {i:v for v,i in nodes.items()}
ranks, sorted_node = zip(*sorted([(x,nodes[i]) for (i,x) in enumerate(P)],reverse = True))

# Chess nodes count

Chess_count = []

j=0
for i in range(n):
    if set(Page_cat[sorted_node[i]]) & set(Chess_Ids):
        j+=1
    Chess_count.append(j)
       
# Plot

print("\nplot7")

plt.figure(figsize=(12,4))
plt.plot(ranks,'b')
plt.ylabel('Proximity to the node Magnus Carlsen')
plt.yscale("log")
plt.xlim(1,1e6)
plt.ylim(1e-6,1e-2)
plt.xscale("log")
plt.grid(True)
plt.savefig('../res/plot7.png')

print("\nplot8")

plt.figure(figsize=(12,4))
plt.plot(Chess_count,'b')
plt.ylabel('Number of Top-K nodes in the category Chess')
plt.xlim(1,1e6)
plt.ylim(0,2500)
plt.xscale("log")
plt.grid(True)
plt.savefig('../res/plot8.png')

# Chess Boxing

Chess_Boxing_ID = 2843859

P0 = np.zeros((n,1))
P0[nodes[Chess_Boxing_ID]]=1

P = personalized_poweriteration(n,matrix,P0,0.15)

# Highest and Lowest
                
nodes = {i:v for v,i in nodes.items()}
ranks, sorted_node = zip(*sorted([(x,nodes[i]) for (i,x) in enumerate(P)],reverse = True))

# Chess nodes count

Boxing_count = []

j=0
for i in range(n):
    if set(Page_cat[sorted_node[i]]) & set(Boxing_Ids):
        j+=1
    Boxing_count.append(j)
       
# Plot

print("\nplot9")

plt.figure(figsize=(12,4))
plt.plot(ranks,'b')
plt.ylabel('Proximity to the node Chess Boxing')
plt.yscale("log")
plt.xlim(1,1e6)
plt.ylim(1e-7,1e-1)
plt.xscale("log")
plt.grid(True)
plt.savefig('../res/plot9.png')

print("\nplot10")

plt.figure(figsize=(12,4))
plt.plot(Boxing_count,'b')
plt.ylabel('Number of Top-K nodes in the category Boxing')
plt.xlim(1,1e6)
plt.ylim(0,3500)
plt.xscale("log")
plt.grid(True)
plt.savefig('../res/plot10.png')