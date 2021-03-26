import numpy as np
import scipy.sparse as sprs
import queue
from tqdm import tqdm

def read_adjmatrix(filename, n, m):

    matrix = sprs.lil_matrix((n, n))
    node = {}
    in_degree = {}
    out_degree = {}

    i = 0

    pbar = tqdm(total=m, position=0, leave=True)
    with open(filename) as file:
        for line in file:
            if not(line.startswith("#")):
                edge = list(map(int, line.split()))
                if edge[0] not in node.keys():
                    in_degree[edge[0]] = 0
                    out_degree[edge[0]] = 0
                    node[edge[0]] = i
                    i += 1
                if edge[1] not in node.keys():
                    in_degree[edge[1]] = 0
                    out_degree[edge[1]] = 0
                    node[edge[1]] = i
                    i += 1
                matrix[node[edge[1]], node[edge[0]]] = 1
                in_degree[edge[1]] += 1
                out_degree[edge[0]] += 1
                pbar.update(1)
        file.close()
        pbar.close()

    diag = sprs.lil_matrix((n, n))
    for i in node.keys():
        if out_degree[i]!=0:
            index = node[i]
            diag[index,index]=1/out_degree[i]
    
    matrix = matrix @ diag
    matrix = matrix.tocsr()

    return matrix, node, in_degree, out_degree

def read_adjmatrix_ungraph(filename, n, m):

    matrix = sprs.lil_matrix((n, n))
    node = {}
    deg = {}
    i = 0

    pbar = tqdm(total=m, position=0, leave=True)
    with open(filename) as file:
        for line in file:
            if not(line.startswith("#")):
                edge = list(map(int, line.split()))
                if edge[0] not in node.keys():
                    deg[edge[0]] = 0
                    node[edge[0]] = i
                    i += 1
                if edge[1] not in node.keys():
                    deg[edge[1]] = 0
                    node[edge[1]] = i
                    i += 1
                if matrix[node[edge[1]], node[edge[0]]]!=1 or matrix[node[edge[0]], node[edge[1]]]!=1:
                    matrix[node[edge[1]], node[edge[0]]] = 1
                    deg[edge[0]] += 1 
                    deg[edge[1]] += 1 
                pbar.update(1)
        file.close()
        pbar.close()
    
    matrix = matrix.tocsr()
    matrix = matrix.transpose() + matrix
    
    diag = sprs.lil_matrix((n, n))
    for i in node.keys():
        if deg[i]!=0:
            index = node[i]
            diag[index,index]=1/deg[i]
    
    matrix = matrix @ diag

    return matrix, node

def read_dag_adjarray(filename):
    nodes={} 
    with open(filename) as file:
        for line in file:
            if not(line.startswith("#")):
                edge=list(map(int,line.split()))
                if edge[0] not in nodes.keys():
                    nodes[edge[0]]=[]
                if edge[1] not in nodes.keys():
                    nodes[edge[1]]=[]
                nodes[edge[0]].append(edge[1])
        file.close()
    deg = {x:len(v) for x,v in nodes.items()}
    return nodes,deg

# Page Graph

file = "../data/raw/alr21--dirLinks--enwiki-20071018.txt"
n = 2070486
m = 46092177

print('\nReading Page Graph...')

matrix,nodes,in_degree,out_degree = read_adjmatrix(file,n,m)
np.save('../data/nodes',nodes)
np.save('../data/in_degree',in_degree)
np.save('../data/out_degree',out_degree)
sprs.save_npz('../data/matrix',matrix)

# Undirected Page Graph

file = "../data/raw/alr21--dirLinks--enwiki-20071018.txt"
n = 2070486
m = 46092177

print('\nReading Undirected Page Graph...')

matrix,nodes = read_adjmatrix_ungraph(file,n,m)
np.save('../data/un_nodes',nodes)
sprs.save_npz('../data/un_matrix',matrix)


# Page_Ids

ID = "../data/raw/alr21--pageNum2Name--enwiki-20071018.txt"

print('\nReading Page Ids...')

page_ids = {}
sep = " "
with open(ID, encoding=('utf-8')) as file:
    for line in file:
        if not(line.startswith("#")):
            row = list(line.split())
            if row!=[]:
               if int(row[0]) not in page_ids.keys():
                  page_ids[int(row[0])]=[]
               page_ids[int(row[0])]=sep.join(row[1:])

np.save('../data/Page_IDs',page_ids)

# Page Categories lists

ID = "../data/raw/alr21--pageCategList--enwiki--20071018.txt"

print('\nReading Categories Lists...')

page_cat = {}
sep = " "
with open(ID, encoding=('utf-8')) as file:
    for line in file:
        if not(line.startswith("#")):
            row = list(map(int, line.split()))
            if row!=[]:
               if row[0] not in page_cat.keys():
                  page_cat[row[0]]=[]
               page_cat[row[0]]=row[1:]

np.save('../data/Page_Cat',page_cat)

# Categories Ids

ID = "../data/raw/alr21--categNum2Name--enwiki-20071018.txt"

print('\nReading Categories Ids...')

cat_ids = {}
sep = " "
with open(ID, encoding=('utf-8')) as file:
    for line in file:
        if not(line.startswith("#")):
            row = list(line.split())
            if row!=[]:
               if int(row[0]) not in cat_ids.keys():
                  cat_ids[int(row[0])]=[]
               cat_ids[int(row[0])]=sep.join(row[1:])

np.save('../data/Cat_ids',cat_ids)

# Categ Graph

print("\nReading Categories Hierarchy...")

filename = "../data/raw/alr21--catHier_allDirLinks--enwiki-20071018.txt"
nodes,deg = read_dag_adjarray(filename)

# Chess Ids

print('\nBuilding Chess Ids...')
Chess_Ids = [691713]
q = queue.Queue()
q.put(691713)

while q.qsize()>0:
    k = q.get()
    for i in nodes[k]:
        if i not in Chess_Ids:
            q.put(i)
            Chess_Ids.append(i)

print(len(Chess_Ids))
Chess_Ids = np.asarray(Chess_Ids)
np.save('../data/Chess_Ids',Chess_Ids)

# Boxing Ids

print('\nBuilding Boxing Ids...')
Boxing_Ids = [738624]
q = queue.Queue()
q.put(738624)

while q.qsize()>0:
    k = q.get()
    for i in nodes[k]:
        if i not in Boxing_Ids:
            q.put(i)
            Boxing_Ids.append(i)

print(len(Boxing_Ids))
Boxing_Ids = np.asarray(Boxing_Ids)
np.save('../data/Boxing_Ids',Boxing_Ids)