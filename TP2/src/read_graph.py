import pickle

def read_adjarray(filename):
    nodes={} 
    print("\nReading...")
    with open(filename) as file:
        for line in file:
            if not(line.startswith("#")):
                edge=list(map(int,line.split()))
                if edge[0] not in nodes.keys():
                    nodes[edge[0]]=[]
                nodes[edge[0]].append(edge[1])
            
                if edge[1] not in nodes.keys():
                    nodes[edge[1]]=[]
                nodes[edge[1]].append(edge[0])
        file.close()
    deg = {x:len(v) for x,v in nodes.items()}
    return nodes,deg


print("\nReading Amazon...")


filename = "../data/raw/com-amazon.ungraph.txt"
nodes,deg = read_adjarray(filename)

print("\nSaving Nodes...")
file = open("../data/Amazon_nodes.bin", "wb")
pickle.dump(nodes, file,)
file.close()
del nodes

print("\nSaving Deg...")
file = open("../data/Amazon_deg.bin", "wb")
pickle.dump(deg, file)
file.close()
del deg


print("\nReading Live Journal...")


filename = "../data/raw/com-lj.ungraph.txt"
nodes,deg = read_adjarray(filename)

print("\nSaving Nodes...")
file = open("../data/lj_nodes.bin", "wb")
pickle.dump(nodes, file,)
file.close()
del nodes

print("\nSaving Deg...")
file = open("../data/lj_deg.bin", "wb")
pickle.dump(deg, file)
file.close()
del deg


print("\nReading Orkut...")


filename = "../data/raw/com-orkut.ungraph.txt"
nodes,deg = read_adjarray(filename)

print("\nSaving Nodes...")
file = open("../data/orkut_nodes.bin", "wb")
pickle.dump(nodes, file)
file.close()
del nodes

print("\nSaving Deg...")
file = open("../data/orkut_deg.bin", "wb")
pickle.dump(deg, file)
file.close()
del deg


print("\nReading Net...")


filename = "../data/raw/net.txt"
nodes,deg = read_adjarray(filename)

print("\nSaving Nodes...")
file = open("../data/net_nodes.bin", "wb")
pickle.dump(nodes, file)
file.close()
del nodes

print("\nSaving Deg...")
file = open("../data/net_deg.bin", "wb")
pickle.dump(deg, file)
file.close()
del deg


print("\nReading Ids...")


ids = []
with open("../data/raw/ID.txt", encoding=('utf-8')) as file:
    for line in file:
        ids.append(line.split())

print("\nSaving Ids...")
file = open("../data/IDs.bin", "wb")
pickle.dump(ids, file)
file.close()
del ids