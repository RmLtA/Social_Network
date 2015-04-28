import snap

Nodes = snap.TIntV()
for nodeId in range(10):
    Nodes.Add(nodeId)

UGraph = snap.GenRndGnm(snap.PUNGraph, 100, 1000)
print snap.GetModularity(UGraph, Nodes, 1000)