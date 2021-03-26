from timeit import default_timer as timer
from tqdm import tqdm
import pickle
import queue

#graph = 'friendster'
#graph = 'lj'
#graph = 'amazon'
#graph = 'orkut'

def k_core_decomposition(n,m,node,deg):
    
    order = {}
    core_value = {}
    cd = []
    
    pbar = tqdm(total = m,position=0,leave=True)
    c = 0

    while(len(deg)>0):
        
        c+=1
        
        q = queue.Queue()
        
        for k,v in deg.items() :
            if v==c :
                q.put(k)
        
        while q.qsize()>0 :

            k = q.get()
            core_value[k] = c
            order[k] = n
            cd.append(m/n)
            n = n - 1
            m = m - deg[k]

            for j in node[k]:
                (node[j]).remove(k)
                deg[j]-=1
                if deg[j] == c :
                    q.put(j)
                pbar.update(1)

            del node[k]
            del deg[k]
            
    pbar.close()
    
    cd = cd[::-1]
    maxdens = max(cd)
    p = [i for i in range(len(cd)) if cd[i]==maxdens][0]+1
    
    print("The core value of the graph is : ", c)
    print("Densest Subgraph : ", [k for k, v in order.items() if v<=p])
    print("The average degree density of a densest core orderin prefix is : ", maxdens)
    print("The edge density of a densest core orderin prefix is : ", 2*maxdens/(p-1))
    print("The size of a densest core ordering prefix is :", p)
    return(order,core_value,cd)

# Loaging Graph

file = open('../data/' + graph + '_nodes.bin', "rb")
nodes = pickle.load(file)
file.close()

file = open('../data/' + graph + '_deg.bin', "rb")
deg = pickle.load(file)
file.close()

n = len(nodes)
m = sum(deg.values())/2

# K-core Decomposition

start = timer()
order, core_value, cd = k_core_decomposition(n, m, nodes, deg)
print("\nProcessing Time : ",timer()-start,"\n")