import re
import os
from snap import *

#This script create an undirected graph from a ".edges" file and show how to add nodes, edges and colours

#Give colours to the graph
NIdColorH = TIntStrH()
list=["green","red","blue","purple","yellow","pink"]

#Reading from file and create an undirected graph, print the graph and the informations 
def createTUNGraph(File):
	GraphTUN = TUNGraph.New()
	
	f = open(File,'r')
	print "Creating nodes and edges from the file ...."
	i=0
	for ligne in f.readlines():
		m = re.search(r"([0-9]+) ([0-9]+)", ligne)
		nId = m.group(1)
		
		if(not GraphTUN.IsNode(int(nId))) :
			GraphTUN.AddNode(int(nId))
			NIdColorH[int(nId)]=list[i%5]
			i=i+1
			
		nId1 = m.group(2)
		if(not GraphTUN.IsNode(int(nId1))) :
			GraphTUN.AddNode(int(nId1))
			NIdColorH[int(nId1)]=list[i%5]
			i=i+1
			
		if(not GraphTUN.IsEdge(int(nId),int(nId1))) : 
			GraphTUN.AddEdge(int(nId),int(nId1))
			
	f.close()
	return GraphTUN
	
if __name__ == "__main__":
	#specify your file here (warning : there is an ambiguity between sys and snap, using argv[] generates errors)
	fic = "3980.edges"
	GraphTUN = createTUNGraph(fic)
	print "Graph: Nodes %d, Edges %d" % (GraphTUN.GetNodes(), GraphTUN.GetEdges())
	PrintInfo(GraphTUN, "Python type PUNGraph", "info-pungraph.txt")
	print "Printing graph ... "
	
	DrawGViz(GraphTUN, gvlDot, "graph3980.png", "graph3980", True, NIdColorH)
	print "Done."