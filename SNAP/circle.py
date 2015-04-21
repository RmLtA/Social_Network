import snap

Graph = snap.GenCircle(snap.PNEANet, 3, 2)
for EI in Graph.Edges():
    print "edge: (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())
	
#generating the png graph	
snap.DrawGViz(Graph, snap.gvlDot, "graph.png", "graph 1")
print "Graph Viz generated ... "
